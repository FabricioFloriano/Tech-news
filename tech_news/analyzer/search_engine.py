# Requisito 7

from datetime import datetime
from tech_news.database import search_news


def search_by_title(title):
    title = title
    results = search_news({"title": {"$regex": title.lower()}})

    return [(searched["title"], searched["url"]) for searched in results]


# Requisito 8
def search_by_date(date):
    try:
        date_format = datetime.strptime(
            date, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida")

    response = []
    news = search_news({"timestamp": date_format})
    for new in news:
        response.append((new["title"], new["url"]))
    return response


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    raise NotImplementedError
