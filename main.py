from config import FEEDS, KEYWORDS, TITLE_BANWORDS, TOP_K

from data.loader import load_articles
from processing.dedup import deduplicate
from processing.filter import is_relevant
from processing.clustering import cluster_articles, pick_representative
from scoring.scorer import score
from utils.text import format_article

from llm.fintech_prompt import build_card


def main():
    print("Loading articles...")
    articles = load_articles(FEEDS)
    print(f"Loaded: {len(articles)}")

    clusters = cluster_articles(articles)
    print(f"Clusters: {len(clusters)}")

    signals = []

    for cluster in clusters:
        rep = pick_representative(cluster)

        rep["score"] = score(rep, cluster_size=len(cluster))
        rep["cluster_size"] = len(cluster)

        signals.append(rep)

    signals = sorted(signals, key=lambda x: x["score"], reverse=True)
    top = signals[:TOP_K]

    print("\n=== TOP SIGNALS ===\n")

    for i, article in enumerate(top, 1):
        print("=" * 60)
        print(f"{i}. {article['title']}")
        print(build_card(article))

if __name__ == "__main__":
    main()