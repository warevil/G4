from learnabc.database import Base
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    # password: str

    class Config():
        orm_mode = True


class Course(BaseModel):
    id: int
    name: str

    class Config():
        orm_mode = True


class RequestUser(BaseModel):
    name: str
    email: str
    password: str

    class Config():
        orm_mode = True


class RequestCourse(BaseModel):
    name: str

    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str
    courses: List[Course] = []

    class Config():
        orm_mode = True


class ShowCourse(BaseModel):
    id: int
    name: str
    creator: User

    class Config():
        orm_mode = True


#  --- Auth


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
