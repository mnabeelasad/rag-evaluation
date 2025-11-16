# ⚖️ RAG Performance Evaluation Dashboard

This project provides a complete pipeline to build, evaluate, and visualize the performance of a Retrieval-Augmented Generation (RAG) application.

It uses **LangChain**, **ChromaDB**, **Ragas**, and **Plotly Dash** to create a production-ready evaluation workflow and dashboard.

---

## 📊 Interactive Dashboard

The dashboard visualizes key RAG performance metrics, enabling in-depth analysis of failed questions, retrieval quality, and overall pipeline health.

![RAG Evaluation Dashboard](assets/dashboard.png)

> Add an image named `dashboard.png` inside the `assets/` folder for this image to display.

---

## ✨ Key Features

- **Complete RAG Pipeline**  
  Ingests custom PDF documents and builds a ChromaDB vector database.

- **Ragas Evaluation Metrics**
  - **Faithfulness**
  - **Answer Relevancy**
  - **Context Precision**
  - **Context Recall**

- **Interactive Plotly Dashboard**  
  A dark-mode dashboard for analyzing evaluation results.

- **Custom Test Sets**  
  Create your own Q&A evaluation datasets.

---

## 🚀 How to Run This Project

### 1. Setup

```bash
# Clone repository
git clone https://github.com/mnabeelasad/rag-evaluation.git
cd rag-evaluation

# Create virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .\.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Add your API key
echo "OPENAI_API_KEY='sk-your-key-here'" > .env


test_df = pd.read_json("data/my_test_set.json")


# Step 1: Build the vector database
python build_database.py

# Step 2: Run Ragas evaluation
python evaluate.py

# Step 3: Launch the dashboard
python dashboard.py

http://127.0.0.1:8050/


/rag-evaluation
│
├── data/                      
│   └── legal_test_set.json
├── results/                   
│   └── evaluation_scores.csv
├── source_documents/          
├── vectorstore/               
├── assets/                 
│   └── dashboard.png
│
├── build_database.py           
├── rag_app.py                  
├── evaluate.py                 
├── dashboard.py               
│
├── requirements.txt           
├── .env                        
└── .gitignore                
