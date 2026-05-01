def score(article):
    text = (article["title"] + " " + article["summary"]).lower()

    score = 0

    if "launch" in text:
        score += 3
    if "new" in text:
        score += 1
    if "regulation" in text:
        score += 4
    if "funding" in text:
        score += 3
    if "partnership" in text:
        score += 2

    score += min(len(text) // 200, 3)

    return score