def is_relevant(article, keywords, title_banwords):
    text = (article["title"] + " " + article["summary"]).lower()
    return any(k in text for k in keywords) and not any(k in article["title"] for k in title_banwords)