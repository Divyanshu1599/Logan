from rag.indexer import search
from core.ai_brain import ai_brain_response

def rag_answer(question: str) -> str:
    docs = search(question, top_k=3)
    MAX_CONTEXT_CHARS = 1200

    if not docs:
        return "I'm sorry, I couldn't find any relevant information in your document to answer that question."
    
    context = "\n\n".join(docs)[:MAX_CONTEXT_CHARS]

    prompt = f"""
You are Logan.


RULES:
- Answer using ONLY the information in the context.
- Be concise and confident.
- Do not add explanations or filler.
- If the answer is not in the context, say:
  "I don't have that information in your documents."

Context: {context}
Question: {question}
Answer:
"""
    
    return ai_brain_response(prompt)