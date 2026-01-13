from sentence_transformers import SentenceTransformer
import numpy as np

# Lightweight, fast, industry-accepted
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None


def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_chunks(chunks: list):
    """
    Input: list of chunks [{section, subsection, text}]
    Output: (embeddings_matrix, metadata_list)
    """
    model = get_embedding_model()

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)

    metadata = []
    for i, chunk in enumerate(chunks):
        metadata.append({
            "id": i,
            "section": chunk["section"],
            "subsection": chunk["subsection"],
            "text": chunk["text"]
        })

    return embeddings, metadata
