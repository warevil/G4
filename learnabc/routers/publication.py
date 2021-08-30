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


"""
Permite crear un anuncio (publicación de tipo 1), para esto
se necesita que el id del curso donde se creará la publicación,
tambien los parametros de RequestAnnouncement como:
- title: str
- description: str
también se necesita que el usuario esté logeado.
"""
@router.post('/announcement/{id_course}', status_code=status.HTTP_201_CREATED)
def create_announcement(
        id_course: int,
        request: schemas.publication.RequestAnnouncement,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    course = db.query(models.Course).filter_by(id=id_course).first() # pragma: no cover

    new_announcement = models.Publication( # pragma: no cover
        title=request.title,
        description=request.description,
        type=1,
        course=course
    )

    db.add(new_announcement) # pragma: no cover
    db.commit() # pragma: no cover
    return {"id": new_announcement.id} # pragma: no cover

"""
Permite crear un material en un curso (del cual tiene id_course como id),
tambien requere un titulo, una descripción, y requiere que el usuario
esté logeado.
"""
@router.post('/material/{id_course}', status_code=status.HTTP_201_CREATED)
def create_material(
        id_course: int,
        request: schemas.publication.RequestAnnouncement,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    course = db.query(models.Course).filter_by(id=id_course).first() # pragma: no cover

    new_material = models.Publication( # pragma: no cover
        title=request.title,
        description=request.description,
        type=2,
        course=course
    )

    db.add(new_material) # pragma: no cover
    db.commit() # pragma: no cover
    return {"id": new_material.id} # pragma: no cover

"""
Permite crear una tarea en un curso (del cual tiene id_course como id)
requiere los siguentes parametros: 
* un titulo 
* una descripción
* requiere que el usuario esté logeado.
"""
@router.post('/assignment/{id_course}', status_code=status.HTTP_201_CREATED)
def create_assignment(
        id_course: int,
        request: schemas.publication.RequestAssignment,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    course = db.query(models.Course).filter_by(id=id_course).first() # pragma: no cover

    if not course: # pragma: no cover
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id_course} not found")

    new_assignment = models.Publication( # pragma: no cover
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

    db.add(new_assignment) # pragma: no cover
    db.commit() # pragma: no cover
    return {"id": new_assignment.id} # pragma: no cover

"""
Permite crear un examen en un curso (el cual tenga como id a course_id)
Requiere los siguentes parametros:
    title: str: El titulo del examen.
    description: str : La descripción del examen.
    date_max: date : La fecha maxima de entrega del examen.
    time_max: time : La hora maxima de entrega del examen.
    score_max: int : La nota maxima de calificacion del examen.
"""
@router.post('/exam/{id_course}', status_code=status.HTTP_201_CREATED)
def create_exam(
        id_course: int,
        request: schemas.publication.RequestExam,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    course = db.query(models.Course).filter_by(id=id_course).first() # pragma: no cover

    new_assignment = models.Publication( # pragma: no cover
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

    db.add(new_assignment) # pragma: no cover
    db.commit() # pragma: no cover
    return {"id": new_assignment.id} # pragma: no cover

"""
Permite postear un comentario, requiere un id el cual 
es el id de la publicación donde postearemos el comentario.
Requiere los siguientes parametros:
    content: str : El contenido del comentario. 

"""
@router.post('/{id}/comment', status_code=status.HTTP_201_CREATED)
def post_comment(
        id: int,
        request: schemas.comment.RequestComment,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    new_comment = models.Comment( # pragma: no cover
        content=request.content,
        user_id=current_user.id,
        publication_id=id
    )

    db.add(new_comment) # pragma: no cover
    db.commit() # pragma: no cover

    return "done" # pragma: no cover

"""
Permite obtener todos los anuncios creados
en todos los cursos
"""
@router.get('/announcement', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_announcements(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(type=1).all()

    return publications

"""
Permite obtener todos los anuncios creados 
en el curso el cual tenga como id course_id
"""
@router.get('/announcement/{course_id}', response_model=List[schemas.base.Publication], status_code=status.HTTP_201_CREATED)
def get_course_announcements(course_id: int, db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(
        type=1, course_id=course_id).all()

    return publications

"""
Permite obtener todos los materiales creados
en todos los cursos
"""
@router.get('/material', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_materials(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(type=2).all()

    return publications

"""
Permite obtener todos los materiales creados 
en el curso el cual tenga como id course_id
"""
@router.get('/material/{course_id}', response_model=List[schemas.base.Publication], status_code=status.HTTP_201_CREATED)
def get_course_materials(course_id: int, db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(
        type=2, course_id=course_id).all()

    return publications

"""
Permite obtener todos las tareas creados
en todos los cursos
"""
@router.get('/assignment', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_assignments(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(type=3).all()

    return publications

"""
Permite obtener todos las tareas creados 
en el curso el cual tenga como id course_id
"""
@router.get('/assignment/{course_id}', response_model=List[schemas.base.Publication], status_code=status.HTTP_201_CREATED)
def get_course_assignments(course_id: int, db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(
        type=3, course_id=course_id).all()

    return publications

"""
Permite obtener todos los examenes creados
en todos los cursos
"""
@router.get('/exam', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_exams(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(type=4).all()

    return publications

"""
Permite obtener todos los examenes creados 
en el curso el cual tenga como id course_id
"""
@router.get('/exam/{course_id}', response_model=List[schemas.base.Publication], status_code=status.HTTP_201_CREATED)
def get_course_exams(course_id: int, db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(
        type=4, course_id=course_id).all()

    return publications

"""
Permite obtener todas las publicationes de todos los tipos
como 1, 2, 3 y 4 y de todos los cursos.
"""
@router.get('/', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_publications(db: Session = Depends(get_db)):

    publications = db.query(models.Publication).all()

    return publications

"""
Permite obtener todas las publicationes de todos los tipos
como 1, 2, 3 y 4 y de un curso en espeficico.
"""
@router.get('/{course_id}', response_model=List[schemas.publication.ShowPublication], status_code=status.HTTP_201_CREATED)
def get_course_publications(course_id: int, db: Session = Depends(get_db)):

    publications = db.query(models.Publication).filter_by(
        course_id=course_id).all()

    return publications