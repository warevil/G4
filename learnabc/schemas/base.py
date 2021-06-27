from learnabc.database import Base
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, time


class Course(BaseModel):
    id: int
    name: str

    class Config():
        orm_mode = True


class User(BaseModel):
    id: int
    name: str
    email: str
    # password: str

    class Config():
        orm_mode = True


class Assignment(BaseModel):
    id: int
    title: str
    description: str
    date: date
    time: time
    type: int
    course: Course

    class Config():
        orm_mode = True
