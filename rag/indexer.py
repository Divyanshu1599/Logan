from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import sqlite3
import os
import numpy as np
from torch import embedding

_search_cache = {}

DB_PATH = "rag/index/rag.db"
MODEL_NAME = "all-MiniLM-L6-v2"

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def init_db():
    os.makedirs("rag/index", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            embedding BLOB
        )
    """)
    conn.commit()
    conn.close()

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80):
    """
    Splits text into chunks of specified size with overlap.
    """
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # Move back by overlap

        if start < 0:
            start = 0

    return chunks

def extract_text_from_pdf(file_path: str) -> str:
    """ 
      Extracts text from a PDF file.
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    
    return text

def add_document(text: str):
    chunks = chunk_text(text)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for chunk in chunks:
        embedding = get_model().encode(chunk).tobytes()
        cur.execute(
        "INSERT INTO documents (content, embedding) VALUES (?, ?)",
        (chunk, embedding)
     )
    conn.commit()
    conn.close()

def add_pdf(file_path: str):
    """ Extracts text from a PDF and index it with chunking."""
    text = extract_text_from_pdf(file_path)

    if not text.strip():
        print(f"No text found in PDF: {file_path}")
        return
    add_document(text)
    print(f"Indexed PDF: {file_path}")

def search(query: str, top_k: int = 3):
    """
    Returns the top_k most relevant documents content for a query.
    """
    cache_key = (query, top_k)
    if cache_key in _search_cache:
        return _search_cache[cache_key]
    
    query_embedding = get_model().encode(query)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT content, embedding FROM documents LIMIT 500")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return []
    
    results = []
    for content, embedding_blob in rows:
        doc_embedding = np.frombuffer(embedding_blob, dtype=np.float32)
        similarity = np.dot(query_embedding, doc_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding))
        results.append((content, similarity))

    results.sort(key=lambda x: x[1], reverse=True)
    final = [content for content, similarity in results[:top_k]]

    _search_cache[cache_key] = final
    return final