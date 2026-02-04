import os
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse
from rag import rag_response, rag_response_stream
from session import add_user_message, add_assistant_message

app = FastAPI()

API_TOKEN = os.getenv("API_TOKEN")

def require_token(authorization: str = Header(None)):
    if API_TOKEN:
        if not authorization or authorization != f"Bearer {API_TOKEN}":
            raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/chat")
def chat(query: str, session_id: str = None, auth: None = Depends(require_token)):
    answer, sources = rag_response(query, session_id=session_id)
    # store messages
    if session_id:
        add_user_message(session_id, query)
        add_assistant_message(session_id, answer)
    return {"response": answer, "sources": sources}

@app.post("/chat/stream")
def chat_stream(query: str, session_id: str = None, auth: None = Depends(require_token)):
    def generator():
        # stream text chunks, then a final JSON line with sources
        for chunk in rag_response_stream(query, session_id=session_id):
            yield chunk
    return StreamingResponse(generator(), media_type="text/plain")
