from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def deduplicate(articles, threshold=0.85):
    texts = [a["title"] + " " + a["summary"] for a in articles]
    embeddings = model.encode(texts)

    used = set()
    unique_articles = []

    for i in range(len(articles)):
        if i in used:
            continue

        for j in range(i + 1, len(articles)):
            sim = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
            if sim > threshold:
                used.add(j)

        unique_articles.append(articles[i])

    return unique_articles