from rag.indexer import search
from core.ai_brain import ai_brain_response

def summarize_pdf(query: str = "summarizer"):
    """
    summarize PDF content using RAG-retrieved chunks.
    """

    # Retrieve relevant chunks (top 5 for summarization)
    docs = search(query, top_k=5)

    if not docs:
        return "I coudln't find any document content to summarize."
    
    context = "\n\n".join(docs)

    prompt = f"""
SYSTEM:
You are Logan.

Summarize the following content clearly and concisely.
Use bullet points.
Do NOT add information that is not present.

CONTENT:
{context}

SUMMARY:
"""
    
    return ai_brain_response(prompt)