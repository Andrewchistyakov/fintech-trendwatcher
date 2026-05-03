from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("intfloat/multilingual-e5-small")

QUERY = """
important fintech news about:
- banking products
- payments
- regulation
- central banks
- fintech startups
- partnerships
- investments
"""

query_emb = model.encode([f"{QUERY}"], normalize_embeddings=True)[0]


def semantic_scores(texts, cluster_size):
    """
    texts: list[str] — статьи из кластера
    """



    docs = [f"{t}" for t in texts]

    emb = model.encode(docs, normalize_embeddings=True)

    # cosine similarity
    scores = emb @ query_emb

    return scores

def score_cluster(cluster, representative):
    text = representative["title"] + " " + representative["summary"]

    # semantic score (один текст)
    score = semantic_scores([text], len(cluster))[0]

    # coverage
    coverage = min(len(cluster) / 3, 1.0)  # нормализация 0–1

    def source_bonus(link):
        if "cbr.ru" in link:
            return 0.2
        if "reuters" in link or "bloomberg" in link:
            return 0.15
        if "rbc.ru" in link:
            return 0.1
        return 0
    
    # source
    src = source_bonus(representative["link"])

    # финальный скор
    final = 0.7 * score + 0.2 * coverage + 0.1 * src

    return float(final)