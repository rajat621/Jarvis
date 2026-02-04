from backend.pinecone_utils import upsert_texts

def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

with open("data/knowledge.txt", encoding="utf-8") as f:
    text = f.read().strip()

chunks = chunk_text(text)
batch = []
for idx, chunk in enumerate(chunks):
    batch.append((f"knowledge_{idx}", chunk, {"source": "knowledge.txt"}))
    if len(batch) >= 50:
        upsert_texts(batch)
        batch = []

if batch:
    upsert_texts(batch)
