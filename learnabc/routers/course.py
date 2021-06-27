from hashlib import new
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, models, oauth2, schemas
# from ..schemas import course, user, base
from sqlalchemy.orm import Session
# from ..repository import blog

router = APIRouter(
    prefix="/course",
    tags=['Course']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_course(
        request: schemas.course.RequestCourse,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    new_course = models.Course(
        name=request.name,
        description=request.description,
        user_id=current_user.id
    )

    db.add(new_course)
    db.commit()
    return {"id": new_course.id}


@router.post('/{id}/{user_id}', status_code=status.HTTP_201_CREATED)
def enroll_user(id: int, user_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=id).first()
    user = db.query(models.User).filter_by(id=user_id).first()
    inscription = models.Inscription(user=user, course=course)
    db.add(inscription)
    db.commit()
    return "done"


@router.post('/{id}/delegate/{user_id}', status_code=status.HTTP_201_CREATED)
def delegate_user(id: int, user_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=id).first()
    user = db.query(models.User).filter_by(id=user_id).first()
    course.delegate = user
    db.commit()
    return "done"


@router.get('/', response_model=List[schemas.course.ShowCourse], status_code=status.HTTP_200_OK)
def all_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses


@router.get('/{id}/inscriptions', response_model=List[schemas.course.InscriptionUser], status_code=status.HTTP_200_OK)
def get_inscriptions(
        id: int,
        db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=id).first()
    return course.inscriptions


@router.get('/{id}', response_model=schemas.course.ShowCourse, status_code=status.HTTP_200_OK)
def get_course(
        id: int,
        db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=id).first()
    return course


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(
        id: int,
        db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=id)
    if not course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    course.delete(synchronize_session=False)
    db.commit()
    return "deleted"


@router.post('/{id}/calification/{user_id}', status_code=status.HTTP_200_OK)
def calificate(id: int, user_id: int,
               request: schemas.course.CalificationRequest,
               db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=id).first()
    user = db.query(models.User).filter_by(id=user_id).first()

    inscription = db.query(models.Inscription).filter_by(
        course=course, user=user).first()
    inscription.calification = request.calification
    db.commit()
    return "done"
