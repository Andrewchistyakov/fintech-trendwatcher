from bs4 import BeautifulSoup
import re

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    # удалить мусорные теги
    for tag in soup(["script", "style", "sup"]):
        tag.decompose()

    text = soup.get_text(" ")

    # спецсимволы
    text = text.replace("\xa0", " ")

    # убрать лишние пробелы
    text = re.sub(r"\s+", " ", text)

    return text[:750].strip()