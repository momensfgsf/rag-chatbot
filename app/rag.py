from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def chunk_text(text, chunk_size=800):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def build_index(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks, convert_to_numpy=True).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return model, index

def search_chunks(question, chunks, model, index, top_k=3):
    q_embed = model.encode([question], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(q_embed, top_k)

    return [chunks[i] for i in indices[0]]