from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

DB_PATH = "vectorstore/db_chroma"

class RealRAGApp:
    def __init__(self):
        # Load the persistent database
        embeddings = OpenAIEmbeddings()
        self.db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        
        # Create the retriever
        self.retriever = self.db.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 chunks
        
        # Define the LLM
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        # Define the prompt template
        template = """
        Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Provide a concise and factual answer.

        Context: {context}

        Question: {question}

        Helpful Answer:
        """
        self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])

        # Create the RAG chain
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def get_rag_response(self, question: str) -> dict:
        """
        Generates a RAG response, including the retrieved contexts.
        """
        # 1. Get the retrieved documents (contexts)
        retrieved_docs = self.retriever.invoke(question)       
        contexts = [doc.page_content for doc in retrieved_docs]
        
        # 2. Get the generated answer
        answer = self.chain.invoke(question)
        
        return {
            "answer": answer,
            "contexts": contexts
        }

# --- This part is to make it easy to use in evaluate.py ---
# We create one instance of the app to be imported
global_rag_app = RealRAGApp()

def get_rag_response(question: str) -> dict:
    """A simple wrapper function for the evaluate.py script."""
    return global_rag_app.get_rag_response(question)