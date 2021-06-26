from fastapi import APIRouter
from ... import database
from .models import User,UserCourses
from .schemas import ShowUser,RequestUser
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from . import queries as user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', response_model=ShowUser)
def create_user(request: RequestUser, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/{id}', response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)
