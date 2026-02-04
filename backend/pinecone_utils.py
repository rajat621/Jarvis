import pinecone, os
from sentence_transformers import SentenceTransformer

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV")
)

model = SentenceTransformer("all-MiniLM-L6-v2")
INDEX_NAME = os.getenv("INDEX_NAME")

def create_index_if_not_exists(name: str, dimension: int = 384, metric: str = "cosine"):
    if name not in pinecone.list_indexes():
        pinecone.create_index(name, dimension=dimension, metric=metric)

# Ensure index exists and initialize it
create_index_if_not_exists(INDEX_NAME, dimension=model.get_sentence_embedding_dimension() if hasattr(model, "get_sentence_embedding_dimension") else 384)
index = pinecone.Index(INDEX_NAME)

def embed(text):
    return model.encode(text).tolist()

def upsert_text(id, text):
    index.upsert([(id, embed(text), {"text": text})])

def upsert_texts(items):
    """Batch upsert. items is a list of (id, text, metadata_dict)."""
    vectors = []
    for _id, txt, metadata in items:
        vectors.append((_id, embed(txt), metadata))
    index.upsert(vectors)

def query_text(query, top_k=3):
    res = index.query(vector=embed(query), top_k=top_k, include_metadata=True)
    matches = []
    for m in res.get("matches", []):
        matches.append({
            "id": m.get("id"),
            "text": m.get("metadata", {}).get("text", ""),
            "score": m.get("score"),
            "metadata": m.get("metadata", {})
        })
    return matches

