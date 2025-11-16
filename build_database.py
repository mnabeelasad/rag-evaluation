from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# Define the path for the persistent database
DB_PATH = "vectorstore/db_chroma"

def create_vector_db():
    print("Loading documents...")
    # Load all PDFs from the source_documents folder
    loader = DirectoryLoader('source_documents/', glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()

    print(f"Loaded {len(documents)} documents.")

    print("Splitting documents into chunks...")
    # Split documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    
    print(f"Split into {len(texts)} chunks.")

    print("Creating embeddings and vector store...")
    # Use OpenAI for embeddings
    embeddings = OpenAIEmbeddings()
    
    # Create a persistent Chroma database
    db = Chroma.from_documents(
        texts, 
        embeddings, 
        persist_directory=DB_PATH
    )
    print("--- Database successfully created! ---")

if __name__ == "__main__":
    create_vector_db()