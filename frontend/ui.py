import streamlit as st
import requests
import uuid
import json

st.title("🤖 Jarvis AI Assistant")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {role, content, sources}

col1, col2 = st.columns([4,1])
with col1:
    query = st.text_input("Ask Jarvis:")
with col2:
    if st.button("Send"):
        pass

def render_messages():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Jarvis:** {msg['content']}")
            if msg.get("sources"):
                with st.expander("Sources"):
                    for s in msg["sources"]:
                        st.write(f"- {s.get('text')[:200]} (score: {s.get('score')})")

render_messages()

if st.button("Send") and query:
    placeholder = st.empty()
    with st.spinner("Thinking..."):
        output = ""
        sources = None
        url = "http://localhost:8000/chat/stream"
        params = {"query": query, "session_id": st.session_state.session_id}
        res = requests.post(url, params=params, stream=True)
        for line in res.iter_lines():
            if not line:
                continue
            text = line.decode()
            # final sources come as a JSON line like {"__sources__": [...]}
            try:
                payload = json.loads(text)
                if "__sources__" in payload:
                    sources = payload["__sources__"]
                    break
            except Exception:
                output += text
                placeholder.markdown(output)
        # append to session messages
        st.session_state.messages.append({"role": "user", "content": query})
        st.session_state.messages.append({"role": "assistant", "content": output, "sources": sources})
        placeholder.empty()
        st.experimental_rerun()