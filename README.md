# Jarvis AI Assistant (Enterprise)

This project implements an enterprise-style personal assistant powered by a self-hosted LLaMA-style LLM, with Pinecone vector DB for retrieval and a conversational Streamlit UI.

Quick start

1. Copy `.env.example` to `.env` and fill in Pinecone keys and `API_TOKEN`.
2. Start Local LLaMA service (LocalAI/text-generation-webui) locally or via Docker (see `docker-compose.yml`).
3. Build and run with Docker Compose: `docker-compose up --build` or run services directly.
4. Ingest knowledge: `python ingest.py`.
5. Visit Streamlit UI at `http://localhost:8501` and chat.

Features

- Self-hosted LLaMA integration (streaming support)
- Pinecone vector DB with chunked ingestion and batch upserts
- RAG integration, including conversation history
- Streaming chat endpoint /chat/stream and non-streaming /chat
- Simple token-based API auth via `API_TOKEN`
- Basic tests and developer Dockerfiles

Notes

- This is a demo. Replace the in-memory session store with Redis for production, and secure secrets appropriately.
