import os

HF_TOKEN = os.getenv("HF_TOKEN")

HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
DB_FAISS_PATH="vectorstore/db_faiss"
DATA_PATH="data/"
CHUNK_SIZE=500
CHUNK_OVERLAP=50

CUSTOM_PROMPT_TEMPLATE = """
Answer the following question in 2-3 lines maximum using only the information provided in the context. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question:
{question}

Answer:
"""
