from learnabc.schemas.publication import ShowAssignment
from typing import List, Optional
from pydantic import BaseModel
from .base import Course, User, Assignment
from datetime import date, time


class RequestSubmission(BaseModel):
    # user_id: int
    publication_id: int


class ShowEvaluation(BaseModel):
    publication: Assignment
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
