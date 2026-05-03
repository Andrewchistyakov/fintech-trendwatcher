from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import numpy as np

from scoring.scorer import semantic_scores

model = SentenceTransformer("all-MiniLM-L6-v2")

def cluster_articles(articles, eps=0.3, min_samples=1):
    texts = [a["title"] + " " + a["summary"] for a in articles]
    embeddings = model.encode(texts)

    clustering = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="cosine"
    ).fit(embeddings)

    labels = clustering.labels_

    clusters = {}
    for idx, label in enumerate(labels):
        clusters.setdefault(label, []).append(articles[idx])

    return list(clusters.values())


def pick_representative(cluster):
    texts = [
        a["title"] + " " + a["summary"]
        for a in cluster
    ]

    scores = semantic_scores(texts, len(cluster))

    def source_bonus(link):
        if "cbr.ru" in link:
            return 0.2
        if "reuters" in link or "bloomberg" in link:
            return 0.15
        if "rbc.ru" in link:
            return 0.1
        return 0

    final_scores = [
        s + source_bonus(a["link"])
        for s, a in zip(scores, cluster)
    ]

    best_idx = max(range(len(cluster)), key=lambda i: final_scores[i])
    return cluster[best_idx]