from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import numpy as np

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
    # простая эвристика — самая длинная статья
    return max(cluster, key=lambda x: len(x["summary"]))