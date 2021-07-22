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
    return user.create(request, db)


@router.get('/', response_model=List[schemas.user.ShowUser], status_code=status.HTTP_200_OK)
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', response_model=schemas.user.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)


@router.get('/byemail/{email}', response_model=schemas.user.ShowUser)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the email {email} is not available")
    return user


@router.put('/{email}')
def edit_user(request: schemas.base.EditUser, email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the email {email} is not available")
    if request.phone:
        user.phone = request.phone
    if request.link:
        user.link = request.link

    db.commit()

    return {'detail': 'done'}
