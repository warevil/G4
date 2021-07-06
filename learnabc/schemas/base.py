from os import name
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date, time


class CourseCode(BaseModel):
    code: str


class User(BaseModel):
    id: int
    name: str
    email: str
    # password: str

    class Config():
        orm_mode = True


class GroupInscriptons(BaseModel):
    user: User

    class Config():
        orm_mode = True


class Group(BaseModel):
    id: int
    name: str
    locked: bool
    inscriptions: List[GroupInscriptons]

    class Config():
        orm_mode = True


class Comment(BaseModel):
    id: int
    user: User
    content: str
    date: date
    time: time

    class Config():
        orm_mode = True


class Evaluation(BaseModel):
    id: int
    date_max: date
    time_max: time
    score_max: int
    group: bool
    comments: List[Comment] = []

    class Config():
        orm_mode = True


class Course(BaseModel):
    id: int
    name: str
    description: str

    class Config():
        orm_mode = True


class Assignment(BaseModel):
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
    id: int
    user: User
    type: int

    class Config():
        orm_mode = True


class Publication(BaseModel):
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
        if v is not None:
            return v

    class Config():
        orm_mode = True
