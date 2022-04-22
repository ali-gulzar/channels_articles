import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def patch_database(mocker):
    def mock_get_channels():
        return [(1, "bbc"), (2, "ary news")]

    mocker.patch("app.services.database.get_channels", new=mock_get_channels)

    def mock_add_channel(query):
        return 10

    mocker.patch("app.services.database.add_channel", new=mock_add_channel)

    def mock_delete_channel(query):
        return

    mocker.patch("app.services.database.delete_channel", new=mock_delete_channel)

    def mock_channel_exists(query):
        return True

    mocker.patch("app.services.database.channel_exists", new=mock_channel_exists)

    def mock_get_articles(query):
        return [(1, "www.google.com", 20)]

    mocker.patch("app.services.database.get_articles", new=mock_get_articles)

    def mock_article_exists(query, query_1):
        return []

    mocker.patch("app.services.database.article_exists", new=mock_article_exists)

    def mock_add_article(query, query_1, query_2):
        return

    mocker.patch("app.services.database.add_article", new=mock_add_article)

    def mock_count_words(query):
        return 10

    mocker.patch("app.services.utils.count_words", new=mock_count_words)

    def mock_get_article(query, query_1):
        return (1, "www.facebook.com", 23)

    mocker.patch("app.services.database.get_article", new=mock_get_article)

    def mock_delete_article(query):
        return

    mocker.patch("app.services.database.delete_article", new=mock_delete_article)


@pytest.mark.usefixtures("patch_database")
class TestChannelArticleController:
    def test_get_channels(self):
        response = client.get("/channels")
        assert response.status_code == 200
        assert response.json() == [
            {"id": 1, "name": "bbc"},
            {"id": 2, "name": "ary news"},
        ]

    def test_add_channel(self):
        response = client.post("/channels", json={"name": "bbc"})
        assert response.status_code == 200
        assert response.json() == {"id": 10, "name": "bbc"}

    def test_delete_channel(self):
        response = client.delete("/channels/10")
        assert response.status_code == 204

    def test_get_articles(self):
        response = client.get("/channels/1/articles")
        assert response.status_code == 200
        assert response.json() == [{"id": 1, "url": "www.google.com", "words": 20}]

    def test_add_article(self):
        response = client.post("/channels/1/articles", json={"url": "www.google.com"})
        assert response.status_code == 200
        assert response.json() == {"url": "www.google.com"}

    def test_get_article(self):
        response = client.get("/channels/1/articles/1")
        assert response.status_code == 200
        assert response.json() == {"id": 1, "url": "www.facebook.com", "words": 23}

    def test_delete_channel(self):
        response = client.delete("/channels/1/articles/1")
        assert response.status_code == 204
