from fastapi import APIRouter, HTTPException
from typing import List
from .. import database, models, schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', response_model=schemas.user.ShowUser)
def create_user(request: schemas.user.RequestUser, db: Session = Depends(get_db)):
    """Permite crear un nuevo usuario es decir registrarlo en el sistema.

    Args:
        request (schemas.user.RequestUser): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Returns:
        [type]: [description]
    """
    return user.create(request, db)


@router.get('/', response_model=List[schemas.user.ShowUser], status_code=status.HTTP_200_OK)
def all_users(db: Session = Depends(get_db)):
    """Permite obtener todos los usuario del sistema

    Args:
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Returns:
        [type]: [description]
    """
    users = db.query(models.User).all()
    return users


@router.get('/{id}', response_model=schemas.user.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    """Permite obtener los detalles de un usuario

    Args:
        id (int): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Returns:
        [type]: [description]
    """
    return user.show(id, db)


@router.get('/byemail/{email}', response_model=schemas.user.ShowUser)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """Permite obtener los datos de un usuario segun el email que se indique.

    Args:
        email (str): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    user = db.query(models.User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the email {email} is not available")
    return user


@router.put('/{email}')
def edit_user(request: schemas.base.EditUser, email: str, db: Session = Depends(get_db)):
    """Permite editar los datos de un usuario

    Args:
        request (schemas.base.EditUser): [description]
        email (str): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    user = db.query(models.User).filter_by(email=email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  # pragma: no cover
                            detail=f"User with the email {email} is not available")
    if request.phone:
        user.phone = request.phone
    if request.link:
        user.link = request.link

    db.commit()

    return {'detail': 'done'}
