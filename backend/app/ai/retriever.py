import faiss
import numpy as np


def build_faiss_index(embeddings: np.ndarray):
    """
    Creates a FAISS index from embeddings
    """
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


def retrieve_top_k(query: str, index, metadata: list, embed_fn, top_k=5):
    """
    Query FAISS and return top-k relevant chunks
    """
    query_embedding = embed_fn([query])
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx])

    return results
