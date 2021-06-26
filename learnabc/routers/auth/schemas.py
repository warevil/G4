from sqlalchemy import Column, Integer, String, ForeignKey, Table
from ...database import Base
from sqlalchemy.orm import relationship
from learnabc.database import Base
from typing import List, Optional
from pydantic import BaseModel

#  --- Auth


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
