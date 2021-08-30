from learnabc.database import Base
from typing import List, Optional, Union
from pydantic import BaseModel, validator


class RequestJoin(BaseModel):
    """
    Schema para RequestJoin

    Args:
        BaseModel ([type]): [description]
   """
    user_email: str
    user_id: int
