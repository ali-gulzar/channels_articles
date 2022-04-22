import requests
from bs4 import BeautifulSoup

import app.models.api as api_models
import app.services.database as database


def count_words(url: str):
    r = requests.get(
        url if ("http://" in url or "https://" in url) else f"http://{url}"
    )
    soup = BeautifulSoup(r.content, "html.parser")

    tag = soup.body
    words = []
    for string in tag.strings:
        words.append(string)

    return len(words)


def article_count_and_put_in_database(
    channel_id: int,
    article: api_models.ArticleRequest,
    action: api_models.Action,
    article_id: int = None,
):
    words = count_words(article.url)
    if action == api_models.Action.CREATE:
        database.add_article(article.url, words, channel_id)
    elif action == api_models.Action.PATCH:
        database.patch_article(article_id, article.url, words, channel_id)
