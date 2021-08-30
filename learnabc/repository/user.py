
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from fastapi import HTTPException, status
from ..hashing import Hash


def create(request: schemas.base.User, db: Session):
    """Crea un nuevo usuario en la base de datos

    Args:
        request (schemas.base.User): [description]
        db (Session): [description]

    Returns:
        [type]: [description]
    """
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password), oauth=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session):
    """
    Obtiene un usuario de la base de datos
    Args:
        id (int): [description]
        db (Session): [description]

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user
