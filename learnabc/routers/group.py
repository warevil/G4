from hashlib import new
import random
import string
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, models, oauth2, schemas
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/group",
    tags=['Group']
)

get_db = database.get_db


@router.post('/create/{course_id}/{name}', status_code=status.HTTP_201_CREATED)
def create_group(course_id: int, name: str, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=course_id).first()
    if name == 'default':
        name = 'Group ' + str(len(course.groups)+1)
    new_group = models.Group(name=name, course_id=course_id)
    db.add(new_group)
    db.commit()
    return new_group.id


@router.post('/join_me/{id}', status_code=status.HTTP_200_OK)
def join_me(
        id: int,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    group = db.query(models.Group).filter_by(id=id).first()

    if group.locked:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='the group has been lock')

    inscription = db.query(models.Inscription).filter_by(
        course_id=group.course.id,
        user_id=current_user.id
    ).first()

    inscription.group = group
    db.commit()
    return 'done'


@router.post('/join/{id}', status_code=status.HTTP_200_OK)
def join(id: int, request: schemas.group.RequestJoin, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter_by(id=id).first()

    if group.locked:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='the group has been lock')

    if (request.user_email):
        user = db.query(models.User).filter_by(
            email=request.user_email).first()
    else:
        user = db.query(models.User).filter_by(id=request.user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user does not exist')

    inscription = db.query(models.Inscription).filter_by(
        user_id=user.id,
        course_id=group.course.id
    ).first()

    inscription.group = group
    db.commit()

    return 'done'


@router.put('/lock/{id}')
def lock_group(id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter_by(id=id).first()
    group.locked = True
    db.commit()
    return 'done'


@router.put('/lock_all/{course_id}')
def lock_group(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=course_id).first()
    for g in course.groups:
        g.locked = True
    db.commit()
    return 'done'


@router.get('/group/{course_id}', response_model=List[schemas.base.Group])
def get_course_groups(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='course does not exist')
    return course.groups


@router.get('/group/inscriptions/{group_id}', response_model=List[schemas.base.GroupInscriptons])
def get_inscriptions(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter_by(id=group_id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='group does not exist')
    return group.inscriptions
