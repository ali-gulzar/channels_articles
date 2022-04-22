from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Response, status

import app.models.api as api_models
import app.services.database as database
from app.services.utils import article_count_and_put_in_database
from app.services.validations import channel_exists, check_duplicate_article

router = APIRouter()


@router.get("/channels", response_model=List[api_models.ChannelResponse])
def get_channels():
    channels = database.get_channels()
    return [api_models.ChannelResponse(id=id, name=channel) for id, channel in channels]


@router.post("/channels", response_model=api_models.ChannelResponse)
def add_channel(channel: api_models.ChannelRequest):
    channel_id = database.add_channel(channel.name)
    return api_models.ChannelResponse(id=channel_id, name=channel.name)


@router.patch("/channels/{channel_id}", response_model=api_models.ChannelResponse)
def update_channel(channel_id: int, channel: api_models.ChannelRequest):
    id = database.patch_channel(channel_id, channel.name)
    return api_models.ChannelResponse(id=id, name=channel.name)


@router.delete("/channels/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel(channel_id: int):
    database.delete_channel(channel_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/channels/{channel_id}/articles", response_model=List[api_models.ArticleRespone]
)
def get_articles(channel_id: int):
    if channel_exists(channel_id):
        articles = database.get_articles(channel_id)
        return [
            api_models.ArticleRespone(id=id, url=url, words=words)
            for id, url, words in articles
        ]


@router.post("/channels/{channel_id}/articles")
async def add_article(
    channel_id: str,
    article: api_models.ArticleRequest,
    background_tasks: BackgroundTasks,
):
    if channel_exists(channel_id) and check_duplicate_article(article.url, channel_id):
        background_tasks.add_task(
            article_count_and_put_in_database,
            channel_id,
            article,
            api_models.Action.CREATE,
        )
        return article


@router.get(
    "/channels/{channel_id}/articles/{article_id}",
    response_model=api_models.ArticleRespone,
)
def get_article(channel_id: str, article_id: str):
    if channel_exists(channel_id):
        article = database.get_article(article_id, channel_id)
        if article:
            id, url, words = article
            return api_models.ArticleRespone(id=id, url=url, words=words)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No article id '{article_id}' exists in channel id '{channel_id}'",
            )


@router.patch(
    "/channels/{channel_id}/articles/{article_id}",
)
def update_article(
    channel_id: int,
    article_id: int,
    article: api_models.ArticleRequest,
    background_tasks: BackgroundTasks,
):
    if channel_exists(channel_id) and check_duplicate_article(article.url, channel_id):
        existing_article = database.get_article(article_id, channel_id)
        if existing_article:
            background_tasks.add_task(
                article_count_and_put_in_database,
                channel_id,
                article,
                api_models.Action.PATCH,
                article_id,
            )
            return article
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No article id '{article_id}' exists in channel id '{channel_id}'",
            )


@router.delete(
    "/channels/{channel_id}/articles/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_article(channel_id: str, article_id: int):
    if channel_exists(channel_id):
        database.delete_article(article_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
