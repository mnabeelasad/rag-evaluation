# ⚖️ Legal RAG Evaluation Project

This project demonstrates how to evaluate a RAG (Retrieval-Augmented Generation) pipeline using a professional legal dataset and the **Ragas** framework.

It measures the performance of the RAG system not just on simple retrieval, but on its ability to understand and reason with complex legal texts.

## 📊 Metrics Explained

We use an "LLM-as-Judge" to score the RAG application on four key metrics:

* **`faithfulness`**: Does the answer hallucinate or make up facts not found in the retrieved contracts/case law?
* **`answer_relevancy`**: Does the answer directly address the legal question asked?
* **`context_precision`**: Is the retrieved legal text relevant? (Measures noise)
* **`context_recall`**: Did the retriever find *all* the necessary clauses/statutes to answer the question?

## 🚀 How to Run This Project

### 1. Set Up Your Environment

First, clone this repository and navigate into the folder:
```bash
git clone [https://github.com/your-username/rag-legal-evaluation.git](https://github.com/your-username/rag-legal-evaluation.git)
cd rag-legal-evaluation
```

Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 2. Set Your OpenAI API Key

The Ragas "LLM-as-Judge" requires an LLM to score the results. You **must** set your OpenAI API key as an environment variable.

**On macOS/Linux:**
```bash
export OPENAI_API_KEY='sk-...'
```

**On Windows (Command Prompt):**
```bash
set OPENAI_API_KEY=sk-...
```

### 3. Run the Evaluation

Now, simply run the `evaluate.py` script:
```bash
python evaluate.py
```

### 4. Check Your Results

The script will:
1.  Load the test set from `data/legal_test_set.json`.
2.  Run the mock RAG app from `rag_app.py` for each question.
3.  Use Ragas to score the outputs.
4.  Print the average scores to your terminal.
5.  Save the detailed, row-by-row scores in `results/evaluation_scores.csv`.

You can now analyze the `.csv` file to see exactly where your RAG app failed and where it succeeded.