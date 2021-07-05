from learnabc.schemas.base import CommentReaction, Publication, User
from learnabc.database import Base
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date, time


class RequestComment(BaseModel):
    content: str


class SubComment(BaseModel):
    id: int
    user: User
    date: date
    time: time
    content: str
    reactions: List[CommentReaction] = []

    class Config():
        orm_mode = True


class ShowCommentPublication(BaseModel):
    id: int
    user: User
    content: str
    date: date
    time: time
    # reactions: List[CommentReaction] = []
    comments: List[SubComment] = []

    class Config():
        orm_mode = True


class ShowComment(BaseModel):
    id: int
    user: User
    publication: Publication
    date: date
    time: time
    content: str
    reactions: List[CommentReaction] = []
    comments: List[ShowCommentPublication] = []

    class Config():
        orm_mode = True
