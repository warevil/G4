from learnabc.schemas.comment import ShowCommentPublication
from typing import List, Optional
from pydantic import BaseModel, validator
from .base import Course, Evaluation
from datetime import date, time


class RequestAnnouncement(BaseModel):
    """
    Schema para RequestAnnouncement

    Args:
        BaseModel ([type]): [description]
   """
    title: str
    description: str


class RequestAssignment(BaseModel):
    """
    Schema para RequestAssignment

    Args:
        BaseModel ([type]): [description]
   """
    title: str
    description: str
    date_max: date
    time_max: time
    score_max: int
    group: bool


class RequestExam(BaseModel):
    """
    Schema para RequestExam

    Args:
        BaseModel ([type]): [description]
   """
    title: str
    description: str
    date_max: date
    time_max: time
    score_max: int


class ShowPublication(BaseModel):
    """
    Schema para ShowPublication

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    title: str
    description: str
    date: date
    time: time
    type: int
    course: Course
    comments: List[ShowCommentPublication] = []
    evaluation: Optional[Evaluation]

    @validator('evaluation')
    def validate_evaluation(cls, v):
        if v is not None: # pragma: no cover
            return v

    class Config():
        orm_mode = True


class ShowAssignment(BaseModel):
    """
    Schema para ShowAssignment

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    title: str
    description: str
    date: date
    time: time
    type: int
    # course: Course
    evaluation: Evaluation

    class Config():
        orm_mode = True
