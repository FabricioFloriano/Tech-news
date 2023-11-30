# Requisito 10
from tech_news.database import find_news


def top_5_categories():
    all_news = find_news()

    category_counts = {}
    for news in all_news:
        category = news["category"]
        category_counts[category] = category_counts.get(category, 0) + 1

    sorted_categories = sorted(
        category_counts.items(), key=lambda x: (-x[1], x[0])
    )

    top_5 = [category for category, _ in sorted_categories[:5]]

    return top_5
