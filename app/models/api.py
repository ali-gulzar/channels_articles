from enum import Enum

from pydantic import BaseModel


class Action(str, Enum):
    CREATE = "create"
    PATCH = "patch"


class Error(BaseModel):
    message: str


class ChannelRequest(BaseModel):
    name: str


class ChannelResponse(ChannelRequest):
    id: int


class ArticleRequest(BaseModel):
    url: str


class ArticleRespone(ArticleRequest):
    id: int
    words: int
