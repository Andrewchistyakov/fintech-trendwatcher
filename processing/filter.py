from datetime import datetime, timedelta


def is_relevant(article):
    now = datetime.utcnow()
    cutoff = now - timedelta(days=7)

    return datetime(*article["published_parsed"][:6]) > cutoff
    
    
    
    