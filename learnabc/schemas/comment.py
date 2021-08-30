from learnabc.schemas.base import CommentReaction, Publication, User
from learnabc.database import Base
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date, time


class RequestComment(BaseModel):
    """
    Schema para RequestComment

    Args:
        BaseModel ([type]): [description]
   """
    content: str


class SubComment(BaseModel):
    """
    Schema para SubComment

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    user: User
    date: date
    time: time
    content: str
    reactions: List[CommentReaction] = []

    class Config():
        orm_mode = True


class ShowCommentPublication(BaseModel):
    """
    Schema para ShowCommentPublication

    Args:
        BaseModel ([type]): [description]
   """
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
    """
    Schema para ShowComment

    Args:
        BaseModel ([type]): [description]
   """
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
