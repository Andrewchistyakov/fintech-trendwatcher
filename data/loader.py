import requests
import feedparser
from utils.clean_text import clean_html

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Accept": "application/rss+xml, application/xml"
}

def load_articles(feeds):
    articles = []

    for url in feeds:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            print(f"{url} -> status {response.status_code}")

            if response.status_code != 200:
                continue
            
            feed = feedparser.parse(response.content)
            print(f"entries: {len(feed.entries)}")

            for entry in feed.entries:
                articles.append({
                    "title": entry.title,
                    "summary": clean_html(entry.summary) if "summary" in entry else "",
                    "link": entry.link,
                    "published_parsed": entry.get("published_parsed")
                })
        

        except Exception as e:
            print(f"Error with {url}: {e}")

    return articles