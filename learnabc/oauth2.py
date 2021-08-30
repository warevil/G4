from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import token
from . import database
from sqlalchemy.orm import Session
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Obtiene el usuario actual de la sesion
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    data = token.verify_token(data, credentials_exception)
    user = db.query(models.User).filter(
        models.User.email == data.email).first()
    return user
