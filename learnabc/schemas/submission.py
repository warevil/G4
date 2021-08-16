from typing import List, Optional
from pydantic import BaseModel
from .base import Course, User, Assignment
from datetime import date, time


class RequestSubmission(BaseModel):
    # user_id: int
    publication_id: int


class ShowAssignment(BaseModel):
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
    publication: ShowAssignment
    date_max: date
    time_max: time

    class Config():
        orm_mode = True


class ShowSubmission(BaseModel):
    user: User
    evaluation: ShowEvaluation
    calification: int

    class Config():
        orm_mode = True
