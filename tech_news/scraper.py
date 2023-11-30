# Requisito 1

import time
from parsel import Selector
from tech_news.database import create_news
import requests


def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3
        )
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    elements_news = selector.css(".entry-thumbnail a::attr(href)").getall()
    print(elements_news)
    return elements_news


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    try:
        next_page_link = selector.css(".pagination .next::attr(href)").get()
        return next_page_link
    except IndexError:
        return None


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)

    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css("h1.entry-title::text").get().strip()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css(
        ".title-author a::text").re_first(r'\b(\w+\s\w+)\b')
    reading_time = int(
        selector.css("li.meta-reading-time::text").re_first(r'\d+')
    )
    summary = (
        selector.css("div.entry-content > p:first-of-type")
        .xpath("string()")
        .get()
        .strip()
    )
    category = selector.css("a.category-style > span.label::text").get()

    scraped_data = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }

    return scraped_data


# Requisito 5
def get_tech_news(amount):
    BASE_URL = 'https://blog.betrybe.com'
    current_url = BASE_URL
    collected_urls = []

    while True:
        page_content = fetch(current_url)
        update_links = scrape_updates(page_content)
        collected_urls.extend(update_links)
        current_url = scrape_next_page_link(page_content)

        if len(collected_urls) >= amount or not current_url:
            break

    news_result = [scrape_news(fetch(url)) for url in collected_urls[:amount]]

    create_news(news_result)

    return news_result
