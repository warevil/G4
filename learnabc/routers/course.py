from hashlib import new
import random
import string
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, models, oauth2, schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/course",
    tags=['Course']
)

get_db = database.get_db

"""
TODO protect endpoints, verify user not modify fields of other user
"""


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

    new_course.code = str(new_course.id) + ''.join(random.choice(string.ascii_uppercase)
                                                   for _ in range(6))

    db.commit()

    return {"id": new_course.id}


@router.post('/{course_code}/enroll_me', status_code=status.HTTP_201_CREATED)
def enroll_me(
        course_code: str,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    course = db.query(models.Course).filter_by(code=course_code).first()
    inscription = db.query(models.Inscription).filter_by(
        user_id=current_user.id, course_id=course.id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"course does not exists!")

    if inscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the user is already enrolled")

    inscription = models.Inscription(user_id=current_user.id, course=course)

    db.add(inscription)
    db.commit()

    return "done"


@router.post('/{id}/enroll/by_id/{user_id}', status_code=status.HTTP_201_CREATED)
def enroll_user(id: int, user_id: int, db: Session = Depends(get_db)):

    course = db.query(models.Course).filter_by(id=id).first()
    user = db.query(models.User).filter_by(id=user_id).first()
    inscription = db.query(models.Inscription).filter_by(
        user_id=user_id, course_id=id).first()

    if not course or not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"course or user does not exists!")
    if inscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the user is already enrolled")

    inscription = models.Inscription(user=user, course=course)
    db.add(inscription)
    db.commit()
    return "done"


@router.post('/{id}/enroll/by_email/{email}', status_code=status.HTTP_201_CREATED)
def enroll_user_by_email(id: int, email: str, db: Session = Depends(get_db)):

    course = db.query(models.Course).filter_by(id=id).first()
    user = db.query(models.User).filter_by(email=email).first()
    inscription = db.query(models.Inscription).filter_by(
        user_id=user.id, course_id=id).first()

    if not course or not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"course or user does not exists!")

    if inscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the user is already enrolled")

    inscription = models.Inscription(user=user, course=course)
    db.add(inscription)
    db.commit()
    return "done"


@router.post('/{id}/delegate/{user_id}', status_code=status.HTTP_201_CREATED)
def delegate_user(id: int, user_id: int, db: Session = Depends(get_db)):

    course = db.query(models.Course).filter_by(id=id).first()
    user = db.query(models.User).filter_by(id=user_id).first()
    inscription = db.query(models.Inscription).filter_by(
        user_id=user_id, course_id=id).first()

    if not course or not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"course or user does not exists!")

    if not inscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the user must be enrolled!")

    course.delegate = user
    db.commit()
    return "done"


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


@router.get('/{id}/code', status_code=status.HTTP_201_CREATED)
def get_code(id: int, db: Session = Depends(get_db)):

    course = db.query(models.Course).filter_by(id=id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found")

    return course.code


@router.get('/{id}/new_code', status_code=status.HTTP_201_CREATED)
def get_new_code(id: int, db: Session = Depends(get_db)):

    course = db.query(models.Course).filter_by(id=id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found")

    new_code = str(course.id) + ''.join(random.choice(string.ascii_uppercase)
                                        for _ in range(8))

    course.code = new_code

    db.commit()

    return course.code


@router.get('/', response_model=List[schemas.course.ShowCourse], status_code=status.HTTP_200_OK)
def all_courses(db: Session = Depends(get_db)):

    courses = db.query(models.Course).all()
    return courses


@router.get('/{id}/inscriptions', response_model=List[schemas.course.InscriptionUser], status_code=status.HTTP_200_OK)
def get_inscriptions(
        id: int,
        db: Session = Depends(get_db)):

    course = db.query(models.Course).filter_by(id=id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found")

    return course.inscriptions


@router.get('/{id}', response_model=schemas.course.ShowCourse, status_code=status.HTTP_200_OK)
def get_course(
        id: int,
        db: Session = Depends(get_db)):

    course = db.query(models.Course).filter_by(id=id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found")

    return course


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(
        id: int,
        db: Session = Depends(get_db)):

    course = db.query(models.Course).filter_by(id=id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found")

    db.delete(course)
    db.commit()

    return "done"


@router.put('/edit/{id}', status_code=status.HTTP_200_OK)
def edit_course(
        id: int,
        request: schemas.course.CourseEdit,
        db: Session = Depends(get_db)):

    course = db.query(models.Course).filter_by(id=id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found")

    course.name = request.name
    course.description = request.description

    db.commit()

    return {'detail': 'done'}
