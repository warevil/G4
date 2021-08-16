from hashlib import new
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import false
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

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id_course} not found")

    new_assignment = models.Publication(
        title=request.title,
        description=request.description,
        type=3,
        course=course,
        evaluation=models.Evaluation(
            date_max=request.date_max,
            time_max=request.time_max,
            score_max=request.score_max,
            group=request.group
        )
    )

    db.add(new_assignment)
    db.commit()
    return {"id": new_assignment.id}


@router.post('/exam/{id_course}', status_code=status.HTTP_201_CREATED)
def create_exam(
        id_course: int,
        request: schemas.publication.RequestExam,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    course = db.query(models.Course).filter_by(id=id_course).first()

    new_assignment = models.Publication(
        title=request.title,
        description=request.description,
        type=4,
        course=course,
        evaluation=models.Evaluation(
            date_max=request.date_max,
            time_max=request.time_max,
            score_max=request.score_max,
            group=False,
        )
    )

    db.add(new_assignment)
    db.commit()
    return {"id": new_assignment.id}


@router.post('/{id}/comment', status_code=status.HTTP_201_CREATED)
def post_comment(
        id: int,
        request: schemas.comment.RequestComment,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    new_comment = models.Comment(
        content=request.content,
        user_id=current_user.id,
        publication_id=id
    )

    db.add(new_comment)
    db.commit()

    return "done"


@router.get('/announcement', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_announcements(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(type=1).all()

    return publications


@router.get('/announcement/{course_id}', response_model=List[schemas.base.Publication], status_code=status.HTTP_201_CREATED)
def get_course_announcements(course_id: int, db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(
        type=1, course_id=course_id).all()

    return publications


@router.get('/material', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_materials(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(type=2).all()

    return publications


@router.get('/material/{course_id}', response_model=List[schemas.base.Publication], status_code=status.HTTP_201_CREATED)
def get_course_materials(course_id: int, db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(
        type=2, course_id=course_id).all()

    return publications


@router.get('/assignment', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_assignments(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(type=3).all()

    return publications


@router.get('/assignment/{course_id}', response_model=List[schemas.base.Publication], status_code=status.HTTP_201_CREATED)
def get_course_assignments(course_id: int, db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(
        type=3, course_id=course_id).all()

    return publications


@router.get('/exam', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_exams(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(type=4).all()

    return publications


@router.get('/exam/{course_id}', response_model=List[schemas.base.Publication], status_code=status.HTTP_201_CREATED)
def get_course_exams(course_id: int, db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(
        type=4, course_id=course_id).all()

    return publications


@router.get('/', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_publications(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).all()

    return publications


@router.get('/{course_id}', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_course_publications(course_id: int, db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(
        course_id=course_id).all()

    return publications