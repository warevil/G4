# from learnabc.schemas import course
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, models, oauth2, schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/submission",
    tags=['Submission']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(
        request: schemas.submission.RequestSubmission,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    publication = db.query(models.Publication).filter_by(
        id=request.publication_id).first()
    evaluation = db.query(models.Evaluation).filter_by(
        publication=publication).first()

    submission = models.Submission(evaluation=evaluation, user=current_user)
    db.add(submission)
    db.commit()

    return {"id": submission.id}


@router.get('/{publication_id}', response_model=List[schemas.submission.ShowSubmission],  status_code=status.HTTP_201_CREATED)
def get_submissions(
        publication_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    publication = db.query(models.Publication).filter_by(
        id=publication_id).first()

    evaluation = db.query(models.Evaluation).filter_by(
        publication=publication).first()

    submissions = db.query(
        models.Submission).filter_by(evaluation=evaluation).all()

    return submissions
