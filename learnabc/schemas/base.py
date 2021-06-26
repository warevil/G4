from learnabc.database import Base
from typing import List, Optional
from pydantic import BaseModel


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
