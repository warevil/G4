from typing import List, Optional
from pydantic import BaseModel
from .base import Course, User, Assignment
from datetime import date, time


class RequestSubmission(BaseModel):
    """
    Schema para RequestSubmission

    Args:
        BaseModel ([type]): [description]
   """
    # user_id: int
    publication_id: int


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
    course: Course

    class Config():
        orm_mode = True


class ShowEvaluation(BaseModel):
    """
    Schema para ShowEvaluation

    Args:
        BaseModel ([type]): [description]
   """
    publication: ShowAssignment
    date_max: date
    time_max: time

    class Config():
        orm_mode = True


class ShowSubmission(BaseModel):
    """
    Schema para ShowSubmission

    Args:
        BaseModel ([type]): [description]
   """
    user: User
    evaluation: ShowEvaluation
    calification: int

    class Config():
        orm_mode = True
