from hashlib import new
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from ..auth import oauth2
from ..user.models import User
from .schemas import Course,RequestCourse,ShowCourse
from ..user.schemas import User,RequestUser,ShowUser
from .models import  Course
from ... import database
from sqlalchemy.orm import Session
# from ..repository import blog

router = APIRouter(
    prefix="/course",
    tags=['Course']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_course(
        request: RequestCourse,
        db: Session = Depends(get_db),
        current_user: User = Depends(oauth2.get_current_user)):

    new_course = Course(name=request.name, user_id=current_user.id)
    db.add(new_course)
    db.commit()
    return "created"


@router.post('/{id}/{user_id}', status_code=status.HTTP_201_CREATED)
def enroll_user(id: int, user_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter_by(id=id).first()
    user = db.query(User).filter_by(id=user_id).first()
    course.users_enrolled.append(user)
    db.commit()
    return "done"


@router.get('/', response_model=List[ShowCourse], status_code=status.HTTP_200_OK)
def all_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses


@router.get('/{id}', response_model=ShowCourse, status_code=status.HTTP_200_OK)
def get_course(
        id: int,
        db: Session = Depends(get_db)):
    course = db.query(Course).filter_by(id=id).first()
    return course


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(
        id: int,
        db: Session = Depends(get_db)):
    course = db.query(Course).filter_by(id=id)
    if not course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    course.delete(synchronize_session=False)
    db.commit()
    return "deleted"
