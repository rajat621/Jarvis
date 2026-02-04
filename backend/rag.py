from pinecone_utils import query_text
from llm import query_llama, query_llama_stream
from typing import Iterator, List, Tuple
from session import get_recent_messages
import json

def build_prompt(context: List[dict], user_query: str, recent_messages: List[dict]) -> str:
    ctx_text = "\n\n".join([m.get("text", "") for m in context])
    history = "\n".join([f"{m['role']}: {m['content']}" for m in recent_messages]) if recent_messages else ""
    prompt = f"""Use the following context to answer the question concisely and cite sources when possible.

Context:
{ctx_text}

Conversation history:
{history}

Question: {user_query}
"""
    return prompt

def format_sources(matches: List[dict]) -> List[dict]:
    # Convert match dicts to a minimal citations list
    sources = []
    for m in matches:
        sources.append({
            "id": m.get("id"),
            "text": m.get("text"),
            "score": m.get("score"),
            "metadata": m.get("metadata", {})
        })
    return sources

def rag_response(user_query: str, session_id: str = None) -> Tuple[str, List[dict]]:
    matches = query_text(user_query)
    recent = get_recent_messages(session_id, limit=6) if session_id else []
    prompt = build_prompt(matches, user_query, recent)
    answer = query_llama(prompt)
    return answer, format_sources(matches)

def rag_response_stream(user_query: str, session_id: str = None) -> Iterator[str]:
    matches = query_text(user_query)
    recent = get_recent_messages(session_id, limit=6) if session_id else []
    prompt = build_prompt(matches, user_query, recent)
    for chunk in query_llama_stream(prompt):
        yield chunk
    # After streaming text, send sources as a final JSON-delimited line
    yield json.dumps({"__sources__": format_sources(matches)})
