from llm.ollama_client import generate

def build_card(article):
    prompt = f"""
Ты аналитик финтех-рынка.
Сделай карточку финтех-новости:

Формат:
Заголовок:
Почему важно:
Категория (регуляция / продукт / рынок / технологии):
Краткое резюме:
Риски / возможности:

Новость:
{article['title']}
{article['summary']}
"""

    return generate(prompt)