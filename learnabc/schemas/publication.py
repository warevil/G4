from typing import List, Optional
from pydantic import BaseModel
from .base import Course
from datetime import date, time


class RequestAnnouncement(BaseModel):
    title: str
    description: str

    class Config():
        orm_mode = True


class RequestAssignment(BaseModel):
    title: str
    description: str
    date_max: date
    time_max: time

    class Config():
        orm_mode = True


class ShowPublication(BaseModel):
    id: int
    title: str
    description: str
    date: date
    time: time
    type: int
    course: Course

    class Config():
        orm_mode = True


class ShowPublication(BaseModel):
    id: int
    title: str
    description: str
    date: date
    time: time
    type: int
    course: Course

    class Config():
        orm_mode = True


class Evaluation(BaseModel):
    date_max: date
    time_max: time

    class Config():
        orm_mode = True


class ShowAssignment(BaseModel):
    id: int
    title: str
    description: str
    date: date
    time: time
    type: int
    course: Course
    evaluation: Evaluation

    class Config():
        orm_mode = True
