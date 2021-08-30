from learnabc.database import Base
from typing import List, Optional
from pydantic import BaseModel


class Login(BaseModel):
    """
    Schema para el login

    Args:
        BaseModel ([type]): [description]
    """
    username: str
    password: str


class Token(BaseModel):
    """
    Schema para el Token

    Args:
        BaseModel ([type]): [description]
    """
    access_token: str
    token_type: str


class TokenOAuth(BaseModel):
    """
    Schema para el TokenOAuth

    Args:
        BaseModel ([type]): [description]
    """
    token: str


class TokenData(BaseModel):
    """
    Schema para el ToeknData
    
    Args:
        BaseModel ([type]): [description]
    """
    email: Optional[str] = None
