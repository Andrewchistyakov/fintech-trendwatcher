from config import FEEDS, KEYWORDS, TITLE_BANWORDS, TOP_K

from data.loader import load_articles
from processing.dedup import deduplicate
from processing.filter import is_relevant
from scoring.scorer import score
from utils.text import format_article


def main():
    print("Loading articles...")
    articles = load_articles(FEEDS)
    print(f"Loaded: {len(articles)}")

    articles = deduplicate(articles)
    print(f"After dedup: {len(articles)}")

    articles = [a for a in articles if is_relevant(a, KEYWORDS, TITLE_BANWORDS)]
    print(f"Relevant: {len(articles)}")

    for a in articles:
        a["score"] = score(a)

    articles = sorted(articles, key=lambda x: x["score"], reverse=True)
    top = articles[:TOP_K]

    print("\n=== TOP SIGNALS ===\n")

    for i, article in enumerate(top, 1):
        print(format_article(article, i))


if __name__ == "__main__":
    main()