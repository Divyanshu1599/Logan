Logan is a local-first personal AI assistant built in Python that combines tool calling, memory, document understanding (RAG), and voice interaction into a single system.
Unlike simple chatbots, Logan is designed as a real system with clear architecture, performance optimizations, and production-style safety practices.

->> Key Features
1. Core Intelligence
Tool calling (email, system info, battery status, browser actions)
Rule-based routing with AI fallback
Fast, responsive interaction (non-blocking voice)

2. Memory
Long-term memory (SQLite)
Episodic memory (tracks actions with timestamps)
Time-based recall (e.g. “what did I do yesterday?”)

4. Document Intelligence (RAG)
Retrieval-Augmented Generation (RAG)
Chunked document indexing with overlap
Local vector search (SQLite + embeddings)
PDF ingestion and understanding
PDF summarization
Grounded answers (no hallucination)

4. Voice
Voice-first interaction
Non-blocking text-to-speech (you can interact while Logan speaks)
Polished voice responses (short, human-friendly)

5. Performance
Lazy loading of embedding models
Cached RAG search results
Optimized retrieval (top_k, prompt size limits)
Fast perceived response time

>>> Project Structure
logan/
 ├─ core/          # Brain, router, AI logic, environment loading
 ├─ commands/      # Tool implementations (email, system, memory, etc.)
 ├─ memory/        # Long-term and episodic memory logic
 ├─ rag/           # RAG indexing, retrieval, summarization
 ├─ voice/         # Speech input/output
 ├─ main.py        # Entry point
 ├─ .gitignore
 └─ requirements.txt
