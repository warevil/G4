from learnabc.database import Base
from typing import List, Optional
from pydantic import BaseModel, validator
from .base import Course


class RequestUser(BaseModel):
    """
    Schema para RequestUser

    Args:
        BaseModel ([type]): [description]
   """
    name: str
    email: str
    password: str

    class Config():
        orm_mode = True


class InscriptionCourse(BaseModel):
    """
    Schema para InscriptionCourse

    Args:
        BaseModel ([type]): [description]
   """
    course: Course

    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    """
    Schema para ShowUser

    Args:
        BaseModel ([type]): [description]
   """
    name: str
    email: str
    phone: str
    link: str
    courses_created: List[Course] = []
    inscriptions: List[InscriptionCourse] = []

    class Config():
        orm_mode = True
