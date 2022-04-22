from fastapi import HTTPException, status

import app.services.database as database


def channel_exists(channel_id: int):
    if database.channel_exists(channel_id):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Channel id '{channel_id}' does not exists.",
        )


def check_duplicate_article(article_url: str, channel_id: int):
    if not database.article_exists(article_url, channel_id):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Article id '{article_url}' already exists in channel '{channel_id}'",
        )
