from learnabc.database import Base
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date, time


class Evaluation(BaseModel):
    date_max: date
    time_max: time
    group: bool

    class Config():
        orm_mode = True


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

    class Config():
        orm_mode = True


class Publication(BaseModel):
    id: int
    title: str
    description: str
    date: date
    time: time
    type: int
    evaluation: Optional[Evaluation]

    @validator('evaluation')
    def validate_evaluation(cls, v):
        if v is not None:
            return v

    class Config():
        orm_mode = True
