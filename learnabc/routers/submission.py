from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, models, oauth2, schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/submission",
    tags=['Submission']
)

get_db = database.get_db


""" 
Para que los alumnos puedan crear entregas a cierta publicación,
para esto la publicación debe ser de un tipo que admita evaluación
ya que la tabla de envios tiene relación directa con la tabla evaluacion.
""" 
@router.post('/', status_code=status.HTTP_201_CREATED)
def create(
        request: schemas.submission.RequestSubmission,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    publication = db.query(models.Publication).filter_by(
        id=request.publication_id).first()
    evaluation = db.query(models.Evaluation).filter_by(
        publication=publication).first()

    submission = db.query(models.Submission).filter_by(
        user_id=current_user.id,
        evaluation_id=evaluation.id
    ).first()

    if (submission):
        return {"detail": "submission already exist!"}

    submission = models.Submission(
        evaluation=evaluation,
        user_id=current_user.id
    )

    db.add(submission)
    db.commit()

    return {"id": submission.id}

'''
Permite obtener los detalles de todas los envios de los alumnos
(solo envia de los alumnos que realizaron algun envio)
'''
@router.get('/{publication_id}', response_model=List[schemas.submission.ShowSubmission],  status_code=status.HTTP_201_CREATED)
def get_submissions(
        publication_id: int,
        db: Session = Depends(get_db)):

    publication = db.query(models.Publication).filter_by(
        id=publication_id).first()

    evaluation = db.query(models.Evaluation).filter_by(
        publication=publication).first()

    submissions = db.query(
        models.Submission).filter_by(evaluation=evaluation).all()

    return submissions

''' 
Permite a un creador de curso (profesor) poder calificar un envio segun el submission_id
'''
@router.post('/{submission_id}/calificate/{nota}', status_code=status.HTTP_201_CREATED)
def calificate_submission(
    submission_id: int,
    nota: int,
    db: Session = Depends(get_db)):

    submission = db.query(models.Submission).filter_by(
        id=submission_id).first()

    submission.calification = nota

    db.commit()

    return {"detail": "done"}

''' 
Permite a un creador de curso (profesor) poder calificar un envio segun el user_id y el publication_id
'''
@router.post('/calificate/{user_id}/{publication_id}/{nota}', status_code=status.HTTP_201_CREATED)
def calificate_submission(
    user_id: int,
    publication_id: int,
    nota: int,
    db: Session = Depends(get_db)):

    publication = db.query(models.Publication).filter_by(
        id=publication_id).first()
    evaluation = db.query(models.Evaluation).filter_by(
        publication=publication).first()

    submission = db.query(models.Submission).filter_by(
        user_id=user_id,
        evaluation_id=evaluation.id
    ).first()

    if not submission:
        return {"detail": "submission does not exist"}

    submission.calification = nota

    db.commit()

    return {"detail": "done"}
