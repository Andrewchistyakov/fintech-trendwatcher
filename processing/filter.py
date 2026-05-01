def is_relevant(article, keywords):
    text = (article["title"] + " " + article["summary"]).lower()
    return any(k in text for k in keywords)