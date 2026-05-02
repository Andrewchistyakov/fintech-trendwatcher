from datetime import datetime, timedelta


def is_relevant(article, keywords, title_banwords):
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=24)

    if datetime(*article["published_parsed"][:6]) < cutoff:
        return False

    text = (article["title"] + " " + article["summary"]).lower()
    return any(k in text for k in keywords) and not any(k in article["title"] for k in title_banwords)