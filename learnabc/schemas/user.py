from learnabc.database import Base
from typing import List, Optional
from pydantic import BaseModel
from .base import Course


class RequestUser(BaseModel):
    name: str
    email: str
    password: str

    class Config():
        orm_mode = True


class InscriptionCourse(BaseModel):
    course: Course

    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str
    courses_created: List[Course] = []
    inscriptions: List[InscriptionCourse] = []

    class Config():
        orm_mode = True
