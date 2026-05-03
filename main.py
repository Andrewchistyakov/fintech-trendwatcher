from config import FEEDS, KEYWORDS, TITLE_BANWORDS, TOP_K

from data.loader import load_articles
# from processing.dedup import deduplicate
from processing.filter import is_relevant
from processing.clustering import cluster_articles, pick_representative
from scoring.scorer import semantic_scores, score_cluster
from utils.text import format_article

from llm.output_prompt import build_card


def main():
    print("Loading articles...")
    articles = load_articles(FEEDS)
    print(f"Loaded: {len(articles)}")

    clusters = cluster_articles(articles)
    print(f"Clusters: {len(clusters)}")

    signals = []
    for cluster in clusters:
        rep = pick_representative(cluster)
        score = score_cluster(cluster, rep)

        signals.append({
            "rep": rep,
            "score": score,
            "size": len(cluster),
            'published_parsed': rep['published_parsed'],
            'link': rep['link']
        })

    signals = sorted(signals, key=lambda x: x["score"], reverse=True)
    print('Signals: ', len(signals))
    relevant = []
    for signal in signals:
        if is_relevant(signal):
            relevant.append(signal)
    print('Relevant articles: ', len(relevant))

    top = relevant[:TOP_K]

    sources = set()
    for a in top:
        sources.add(a['link'])

    print("\n=== TOP SIGNALS ===\n")
    text = ''

    for i, article in enumerate(top, 1):
        art = article['rep']
        text += f"{i}. {art['title']}\n"
        text += art['summary'] + '\n'
    
    print(build_card(text))
    print('=== SOURCES === \n')
    for s in sources:
        print(s)
    

if __name__ == "__main__":
    main()