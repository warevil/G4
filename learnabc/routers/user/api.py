from fastapi import APIRouter
from learnabc import schemas
from learnabc.base import database
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from learnabc.routers.user import queries as user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    return user.show(id, db)