from os import name
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date, time


class EditUser(BaseModel):
    """
    Schema para EditUser

    Args:
        BaseModel ([type]): [description]
    """
    phone: str
    link: str


class CourseCode(BaseModel):
    """
    Schema para CourseCode

    Args:
        BaseModel ([type]): [description]
   """
    code: str


class User(BaseModel):
    """
    Schema para User

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    name: str
    email: str
    # password: str

    class Config():
        orm_mode = True


class GroupInscriptons(BaseModel):
    """
    Schema para GroupInscriptons

    Args:
        BaseModel ([type]): [description]
   """
    user: User

    class Config():
        orm_mode = True


class Group(BaseModel):
    """
    Schema para Group

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    name: str
    locked: bool
    inscriptions: List[GroupInscriptons]

    class Config():
        orm_mode = True


class Comment(BaseModel):
    """
    Schema para Comment

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    user: User
    content: str
    date: date
    time: time

    class Config():
        orm_mode = True


class Evaluation(BaseModel):
    """
    Schema para Evaluation

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    date_max: date
    time_max: time
    score_max: int
    group: bool
    comments: List[Comment] = []

    class Config():
        orm_mode = True


class Course(BaseModel):
    """
    Schema para Course

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    name: str
    description: str

    class Config():
        orm_mode = True


class Assignment(BaseModel):
    """
    Schema para Assignment

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    title: str
    description: str
    date: date
    time: time
    type: int
    comments: List[Comment] = []

    class Config():
        orm_mode = True


class CommentReaction(BaseModel):
    """
    Schema para CommentReaction

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    user: User
    type: int

    class Config():
        orm_mode = True


class Publication(BaseModel):
    """
    Schema para Publication

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    title: str
    description: str
    date: date
    time: time
    type: int
    comments: List[Comment] = []
    evaluation: Optional[Evaluation]

    @validator('evaluation')
    def validate_evaluation(cls, v):
        if v is not None: # pragma: no cover
            return v

    class Config():
        orm_mode = True
