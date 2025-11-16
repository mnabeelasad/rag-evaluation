Here is a complete, professional `README.md` file for your project.

You can copy and paste this entire block of code. I have included the screenshot, the technologies, and the step-by-step instructions.

-----

````markdown
# ⚖️ Professional RAG Evaluation Project

This project demonstrates a complete, professional pipeline for building, evaluating, and visualizing the performance of a Retrieval-Augmented Generation (RAG) application.

It uses a real vector database (**ChromaDB**), a **LangChain**-based RAG pipeline, and the **Ragas** framework to quantitatively measure performance. The results are displayed in an interactive **Plotly Dash** dashboard.

---

## 📊 Evaluation Dashboard

The interactive dashboard (built with Plotly Dash) automatically loads the evaluation results to visualize performance. It features average scores for key metrics, a detailed data table, and an interactive filter to analyze low-scoring or "failed" questions.

![RAG Evaluation Dashboard](assets/dashboard.png)

---

## ✨ Key Features

* **Real RAG Pipeline:** Uses **LangChain** and **ChromaDB** to perform RAG on a custom library of PDF documents.
* **Quantitative Evaluation:** Uses the **Ragas** framework to score the pipeline on the four crucial metrics:
    * **`Faithfulness`**: Measures how factually accurate the answer is (reduces hallucinations).
    * **`Answer Relevancy`**: Measures how relevant the answer is to the question.
    * **`Context Precision`**: Measures the signal-to-noise ratio of retrieved documents.
    * **`Context Recall`**: Measures if all necessary information was retrieved.
* **Interactive Dashboard:** A professional **Plotly Dash** application in dark mode to analyze and filter results.
* **Decoupled & Testable:** The project is modular, splitting logic into:
    1.  `build_database.py`: To ingest and index documents.
    2.  `rag_app.py`: The RAG application logic.
    3.  `evaluate.py`: The "testing" script.
    4.  `dashboard.py`: The "results" viewer.

---

## 🚀 How to Run This Project

### 1. Clone the Repository
```bash
git clone [https://github.com/mnabeelasad/rag-evaluation.git](https://github.com/mnabeelasad/rag-evaluation.git)
cd rag-evaluation
````

### 2\. Set Up the Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate
# (Windows)
# .\.venv\Scripts\activate

# Install all required libraries
pip install -r requirements.txt
```

### 3\. Set Your API Key

Create a file named `.env` in the project folder and add your OpenAI API key:

```
OPENAI_API_KEY="sk-..."
```

### 4\. Add Your Knowledge (The "Brain")

Place your own PDF files into the `/source_documents/` folder.

### 5\. Create Your Test Set (The "Exam")

This is the most important step. You must create test questions that match your PDFs.

1.  Create a new file `data/my_test_set.json` (you can copy `data/legal_test_set.json` as a template).
2.  Open your PDFs and write your own `question` and `ground_truth_answer` pairs based on the content.
3.  Open `evaluate.py` and change **one line** to use your new file:
    ```python
    # Find this line:
    test_df = pd.read_json("data/legal_test_set.json")
    # Change it to:
    test_df = pd.read_json("data/my_test_set.json")
    ```

### 6\. Run the Full Pipeline

Run these commands in order:

```bash
# 1. Create the vector database from your PDFs
python build_database.py

# 2. Run the evaluation to generate scores
python evaluate.py

# 3. View the results in your browser
python dashboard.py
```

Now, open `http://127.0.0.1:8050/` in your web browser to see your live dashboard.

-----

## 📂 Project Structure

```
/rag-evaluation
│
├── .venv/                      # Virtual environment
├── data/                       # Test sets (JSON)
│   └── legal_test_set.json
│   └── my_test_set.json
├── results/                    # Output scores
│   └── evaluation_scores.csv
├── source_documents/           # Your PDFs (The "Brain")
│   └── (Your PDFs go here)
├── vectorstore/                # The vector database
│   └── db_chroma/
├── assets/                     # For images
│   └── dashboard.png
│
├── build_database.py           # Script to create the vector DB
├── rag_app.py                  # The RAG application
├── evaluate.py                 # The Ragas evaluation script
├── dashboard.py                # The Plotly Dash dashboard
│
├── requirements.txt            # Python libraries
├── .env                        # Secret API key
└── .gitignore                  # Hides .venv and .env
```

```
```