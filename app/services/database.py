import sqlite3
from typing import Dict, List, Tuple

cursor = None
connection = None

# Channels
GET_CHANNELS_SQL = "SELECT id, name FROM channels"
ADD_CHANNEL_SQL = "INSERT INTO channels VALUES (?, ?) RETURNING id"
PATCH_CHANNEL_SQL = "UPDATE channels SET name = (?) WHERE id = (?) RETURNING id"
DELETE_CHANNEL_SQL = "DELETE FROM channels WHERE id = (?)"
CHANNEL_EXISTS_SQL = "SELECT id FROM channels WHERE id = (?)"

# Articles
GET_ARTICLE_SQL = (
    "SELECT id, url, words FROM articles WHERE id = (?) AND channel_id = (?)"
)
ADD_ARTICLE_SQL = "INSERT INTO articles VALUES (?, ?, ?, ?) RETURNING id"
PATCH_ARTICLE_SQL = (
    "UPDATE articles SET url = (?), words = (?) WHERE channel_id = (?) AND id = (?)"
)
DELETE_ARTICLE_SQL = "DELETE FROM articles WHERE id = (?)"
GET_ARTICLES_SQL = "SELECT id, url, words FROM articles WHERE channel_id = (?)"
ARTICLE_EXISTS_SQL = "SELECT id FROM articles WHERE url = (?) AND channel_id = (?)"


def connect_to_db():
    global cursor
    global connection
    connection = sqlite3.connect("sqlite.db", check_same_thread=False)
    cursor = connection.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON")


def close_connection():
    global connection
    connection.close()


def create_table():
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS channels (id integer primary key autoincrement, name text unique)"
    )
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS articles (id integer primary key autoincrement, url text, words integer, channel_id text, foreign key (channel_id) references channels (id) on delete cascade)"
    )
    connection.commit()


def _query_db(query: str, params: Dict = {}, fetch_one: bool = False):
    cursor.execute(query, params)
    if fetch_one:
        rows = cursor.fetchone()
    else:
        rows = cursor.fetchall()
    return rows


def add_channel(channel_id: int):
    (id,) = _query_db(ADD_CHANNEL_SQL, (None, channel_id), fetch_one=True)
    connection.commit()
    return id


def patch_channel(channel_id: int, channel_name: str):
    (id,) = _query_db(PATCH_CHANNEL_SQL, (channel_name, channel_id), fetch_one=True)
    connection.commit()
    return id


def delete_channel(channel_id: int):
    _query_db(DELETE_CHANNEL_SQL, (channel_id,))
    connection.commit()


def get_channels() -> List[Tuple[str]]:
    return _query_db(GET_CHANNELS_SQL)


def channel_exists(channel_id: int):
    return _query_db(CHANNEL_EXISTS_SQL, (channel_id,))


def get_articles(channel_id: int):
    return _query_db(GET_ARTICLES_SQL, (channel_id,))


def get_article(article_id: int, channel_id: int):
    return _query_db(GET_ARTICLE_SQL, (article_id, channel_id), fetch_one=True)


def add_article(article_url: str, words: int, channel_id: int):
    _query_db(ADD_ARTICLE_SQL, (None, article_url, words, channel_id))
    connection.commit()


def patch_article(article_id: int, article_url: str, words: int, channel_id: int):
    _query_db(PATCH_ARTICLE_SQL, (article_url, words, channel_id, article_id))
    connection.commit()


def delete_article(article_id: int):
    _query_db(DELETE_ARTICLE_SQL, (article_id,))
    connection.commit()


def article_exists(article_url: str, channel_id: int):
    return _query_db(ARTICLE_EXISTS_SQL, (article_url, channel_id))
