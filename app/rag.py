from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# 1) Split big text into chunks
def chunk_text(text, chunk_size=800):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks


# 2) Create embeddings + FAISS search index
def build_index(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)

    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return model, index


# 3) Search best chunks for a question
def search_chunks(question, chunks, model, index, top_k=3):
    q_embed = model.encode([question])
    q_embed = np.array(q_embed).astype("float32")

    distances, indices = index.search(q_embed, top_k)

    results = []
    for i in indices[0]:
        results.append(chunks[i])

    return results