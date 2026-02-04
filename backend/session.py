from collections import deque
from typing import List, Dict

# Simple in-memory session store. For production, replace with Redis or DB.
_sessions: Dict[str, deque] = {}

def _ensure_session(session_id: str):
    if session_id not in _sessions:
        _sessions[session_id] = deque(maxlen=50)

def add_user_message(session_id: str, content: str):
    _ensure_session(session_id)
    _sessions[session_id].append({"role": "user", "content": content})

def add_assistant_message(session_id: str, content: str):
    _ensure_session(session_id)
    _sessions[session_id].append({"role": "assistant", "content": content})

def get_recent_messages(session_id: str, limit: int = 6) -> List[dict]:
    if not session_id or session_id not in _sessions:
        return []
    # return last `limit` messages
    msgs = list(_sessions[session_id])
    return msgs[-limit:]
