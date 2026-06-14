import numpy as np
from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def get_embedding(text: str, api_key: str) -> list[float]:
    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    vector_a = np.array(a)
    vector_b = np.array(b)

    if np.linalg.norm(vector_a) == 0 or np.linalg.norm(vector_b) == 0:
        return 0.0

    return float(np.dot(vector_a, vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b)))


def search_screenshots(query: str, records: list[dict], api_key: str, top_k: int = 5) -> list[dict]:
    if not records:
        return []

    query_embedding = get_embedding(query, api_key)

    scored = []
    for record in records:
        embedding = record.get("embedding")
        if not embedding:
            continue

        score = cosine_similarity(query_embedding, embedding)
        scored.append({**record, "score": score})

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]
