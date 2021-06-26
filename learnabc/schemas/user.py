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


class ShowUser(BaseModel):
    name: str
    email: str
    courses: List[Course] = []
    courses_enrolled: List[Course] = []

    class Config():
        orm_mode = True
