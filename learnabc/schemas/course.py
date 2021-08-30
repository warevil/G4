from learnabc.database import Base
from typing import List, Optional, Union
from pydantic import BaseModel, validator
from .base import Group, User


class CourseEdit(BaseModel):
    """
    Schema para CourseEdit

    Args:
        BaseModel ([type]): [description]
   """
    name: str
    description: str


class UserEmail(BaseModel):
    """
    Schema para UserEmail

    Args:
        BaseModel ([type]): [description]
   """
    email: str


class RequestCourse(BaseModel):
    """
    Schema para RequestCourse

    Args:
        BaseModel ([type]): [description]
   """
    name: str
    description: str


class InscriptionUser(BaseModel):
    """
    Schema para InscriptionUser

    Args:
        BaseModel ([type]): [description]
   """
    user: User
    calification: int

    class Config():
        orm_mode = True


class ShowCourse(BaseModel):
    """
    Schema para ShowCourse

    Args:
        BaseModel ([type]): [description]
   """
    id: int
    name: str
    description: str
    creator: User
    code: Optional[str]
    delegate: Optional[User]
    inscriptions: List[InscriptionUser] = []
    groups: List[Group] = []

    @validator('delegate', 'code')
    def valid_delegate(cls, v):
        if v is not None:
            return v

    class Config():
        orm_mode = True


class CalificationRequest(BaseModel):
    """
    Schema para CalificationRequest

    Args:
        BaseModel ([type]): [description]
   """
    calification: int
