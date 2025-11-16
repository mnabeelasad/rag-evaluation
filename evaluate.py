import os
from dotenv import load_dotenv  # <-- Loads your API key

load_dotenv()  # <-- Reads the .env file

import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
from langchain_openai import ChatOpenAI  # <-- IMPORT THE OPENAI CHAT MODEL

# Import your RAG function
from rag_app import get_rag_response

# --- 1. DEFINE THE "LLM-as-Judge" ---
# This part is still correct.
judge_llm = ChatOpenAI(model="gpt-3.5-turbo")

# Ensure the results directory exists
os.makedirs("results", exist_ok=True)

# --- 2. Load your test dataset ---
print("Loading legal test dataset...")
test_df = pd.read_json("data/legal_test_set.json")

# --- 3. Run your RAG pipeline on each question ---
print("Running RAG pipeline on test questions...")
results = []
for index, row in test_df.iterrows():
    question = row['question']
    response = get_rag_response(question)
    
    results.append({
        "question": question,
        "ground_truth": row['ground_truth_answer'],
        "answer": response['answer'],
        "contexts": response['contexts']
    })

results_df = pd.DataFrame(results)

# --- 4. Convert to Hugging Face Dataset format ---
dataset = Dataset.from_pandas(results_df)

# --- 5. Define the metrics to compute ---
# CHANGED: We go back to the simple list, without .evolve()
metrics_to_run = [
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
]

# --- 6. Run the evaluation ---
print("Running RAG evaluation (this may take a few minutes)...")
# CHANGED: We pass the 'judge_llm' directly into the evaluate function
result = evaluate(
    dataset=dataset,
    metrics=metrics_to_run,
    llm=judge_llm  # <-- THIS IS THE FIX FOR YOUR RAGAS VERSION
)

# --- 7. Save and print the results ---
print("Evaluation complete. Saving results...")
evaluation_df = result.to_pandas()
evaluation_df.to_csv("results/evaluation_scores.csv", index=False)

print("\n--- Individual Scores ---")
print(evaluation_df)

print("\n--- Average Scores ---")
# Get the names of the metrics we just ran
metric_names = [m.name for m in metrics_to_run]

# Calculate and print the average *only* for the metric columns
average_scores = evaluation_df[metric_names].mean()
print(average_scores)