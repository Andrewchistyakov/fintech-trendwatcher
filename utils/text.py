def format_article(article, idx):
    return f"""
{idx}. {article['title']}
Score: {article['score']}
Link: {article['link']}
{'-'*50}
"""