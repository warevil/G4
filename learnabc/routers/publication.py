from hashlib import new
# from learnabc.schemas import course
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, models, oauth2, schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/publication",
    tags=['Publication']
)

get_db = database.get_db


@router.post('/announcement/{id_course}', status_code=status.HTTP_201_CREATED)
def create_announcement(
        id_course: int,
        request: schemas.publication.RequestAnnouncement,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    course = db.query(models.Course).filter_by(id=id_course).first()

    new_announcement = models.Publication(
        title=request.title,
        description=request.description,
        type=1,
        course=course
    )

    db.add(new_announcement)
    db.commit()
    return {"id": new_announcement.id}


@router.post('/material/{id_course}', status_code=status.HTTP_201_CREATED)
def create_material(
        id_course: int,
        request: schemas.publication.RequestAnnouncement,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    course = db.query(models.Course).filter_by(id=id_course).first()

    new_material = models.Publication(
        title=request.title,
        description=request.description,
        type=2,
        course=course
    )

    db.add(new_material)
    db.commit()
    return {"id": new_material.id}


@router.post('/assignment/{id_course}', status_code=status.HTTP_201_CREATED)
def create_assignment(
        id_course: int,
        request: schemas.publication.RequestAssignment,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    course = db.query(models.Course).filter_by(id=id_course).first()

    new_assignment = models.Publication(
        title=request.title,
        description=request.description,
        type=3,
        course=course,
        evaluation=models.Evaluation(
            date_max=request.date_max,
            time_max=request.time_max,
        )
    )

    db.add(new_assignment)
    db.commit()
    return {"id": new_assignment.id}


@router.get('/announcements', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_announcements(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(type=1).all()

    return publications


@router.get('/material', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_materials(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(type=2).all()

    return publications


@router.get('/assignment', response_model=List[schemas.publication.ShowAssignment], status_code=status.HTTP_201_CREATED)
def get_assignments(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(type=3).all()

    return publications


@router.get('/{id}', response_model=schemas.publication.ShowPublication, status_code=status.HTTP_201_CREATED)
def get_publication(
        id: int,
        db: Session = Depends(get_db)):

    publication = db.query(models.Publication).filter_by(id=id).first()

    return publication


@router.get('/', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_publications(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).all()

    return publications
