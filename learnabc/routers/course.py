from hashlib import new
import random
import string
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, models, oauth2, schemas
from sqlalchemy.orm import Session
import rstr

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
    """Permite crear un curso

    Args:
        request (schemas.course.RequestCourse): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).
        current_user (schemas.base.User, optional): [description]. Defaults to Depends(oauth2.get_current_user).

    Returns:
        [type]: [description]
    """
    new_course = models.Course(
        name=request.name,
        description=request.description,
        user_id=current_user.id
    )

    db.add(new_course)
    db.commit()

    new_course.code = str(new_course.id) + rstr.rstr(string.ascii_uppercase, 8)

    db.commit()

    return {"id": new_course.id}

def check_and_raise(check, exception):
    if check: raise exception

@router.post('/{course_code}/enroll_me', status_code=status.HTTP_201_CREATED)
def enroll_me(
        course_code: str,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):
    """Permite matricular a un usuario

    Args:
        course_code (str): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).
        current_user (schemas.base.User, optional): [description]. Defaults to Depends(oauth2.get_current_user).

    Raises:
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    course = db.query(models.Course).filter_by(code=course_code).first()
    inscription = db.query(models.Inscription).filter_by(
        user_id=current_user.id, course_id=course.id).first()


    check_and_raise(
        not course,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail=f"course does not exists!"),
        )
    
    check_and_raise(
        inscription,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the user is already enrolled")
        )

    inscription = models.Inscription(user_id=current_user.id, course=course) # pragma: no cover

    db.add(inscription) # pragma: no cover
    db.commit() # pragma: no cover

    return "done" # pragma: no cover


@router.post('/{id}/enroll/by_id/{user_id}', status_code=status.HTTP_201_CREATED)
def enroll_user(id: int, user_id: int, db: Session = Depends(get_db)):
    """Permite matricular a un usuario

    Args:
        id (int): [description]
        user_id (int): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    course = db.query(models.Course).filter_by(id=id).first()
    user = db.query(models.User).filter_by(id=user_id).first()
    inscription = db.query(models.Inscription).filter_by(
        user_id=user_id, course_id=id).first()

    check_and_raise(
        not course or not user,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail=f"course or user does not exists!")
    )

    check_and_raise(
        inscription,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,  # pragma: no cover
                            detail=f"the user is already enrolled")
    )


    inscription = models.Inscription(user=user, course=course)
    db.add(inscription)
    db.commit()
    return "done"


@router.post('/{id}/enroll/by_email/{email}', status_code=status.HTTP_201_CREATED)
def enroll_user_by_email(id: int, email: str, db: Session = Depends(get_db)):
    """Permite matricular a un usuario segun su email

    Args:
        id (int): [description]
        email (str): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    course = db.query(models.Course).filter_by(id=id).first()
    user = db.query(models.User).filter_by(email=email).first()
    inscription = db.query(models.Inscription).filter_by(
        user_id=user.id, course_id=id).first()

    check_and_raise(
        not course or not user,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail=f"course or user does not exists!")
    )

    check_and_raise(
        inscription,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail=f"the user is already enrolled")
    )

    inscription = models.Inscription(user=user, course=course)
    db.add(inscription)
    db.commit()
    return "done"


@router.post('/{id}/delegate/{user_id}', status_code=status.HTTP_201_CREATED)
def delegate_user(id: int, user_id: int, db: Session = Depends(get_db)):
    """Permite asignar a un alumno como deledado

    Args:
        id (int): [description]
        user_id (int): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    course = db.query(models.Course).filter_by(id=id).first()
    user = db.query(models.User).filter_by(id=user_id).first()
    inscription = db.query(models.Inscription).filter_by(
        user_id=user_id, course_id=id).first()

    check_and_raise(
        not course or not user,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail=f"course or user does not exists!")
    )
    
    check_and_raise(
        not inscription,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail=f"the user must be enrolled!")
    )

    course.delegate = user
    db.commit()
    return "done"


@router.post('/{id}/calification/{user_id}', status_code=status.HTTP_200_OK)
def calificate(id: int, user_id: int,
               request: schemas.course.CalificationRequest,
               db: Session = Depends(get_db)):
    """Permite calificar a un alumno para colocar su nota final del curso

    Args:
        id (int): [description]
        user_id (int): [description]
        request (schemas.course.CalificationRequest): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Returns:
        [type]: [description]
    """
    course = db.query(models.Course).filter_by(id=id).first()
    user = db.query(models.User).filter_by(id=user_id).first()

    inscription = db.query(models.Inscription).filter_by(
        course=course, user=user).first()
    inscription.calification = request.calification
    db.commit()
    return "done"


@router.get('/{id}/code', status_code=status.HTTP_201_CREATED)
def get_code(id: int, db: Session = Depends(get_db)):
    """Permite obtener el codigo de un curso

    Args:
        id (int): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    course = db.query(models.Course).filter_by(id=id).first()

    check_and_raise(
        not course,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found")
    )

    return course.code


@router.get('/{id}/new_code', status_code=status.HTTP_201_CREATED)
def get_new_code(id: int, db: Session = Depends(get_db)):
    """Permite generar un nuevo codigo del curso y obtenerlo.

    Args:
        id (int): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    course = db.query(models.Course).filter_by(id=id).first()

    check_and_raise(
        not course,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found")
    )

    new_code = str(course.id) + rstr.rstr(string.ascii_uppercase, 8)

    course.code = new_code

    db.commit()

    return course.code


@router.get('/', response_model=List[schemas.course.ShowCourse], status_code=status.HTTP_200_OK)
def all_courses(db: Session = Depends(get_db)):
    """Permite obtener todos los cursos creados por todos los usuarios

    Args:
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Returns:
        [type]: [description]
    """
    courses = db.query(models.Course).all()
    return courses


@router.get('/{id}/inscriptions', response_model=List[schemas.course.InscriptionUser], status_code=status.HTTP_200_OK)
def get_inscriptions(
        id: int,
        db: Session = Depends(get_db)):
    """Permite obtener todas las inscriptiones de un curso en especifico.

    Args:
        id (int): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    course = db.query(models.Course).filter_by(id=id).first()

    check_and_raise(
        not course,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found")
    )

    return course.inscriptions


@router.get('/{id}', response_model=schemas.course.ShowCourse, status_code=status.HTTP_200_OK)
def get_course(
        id: int,
        db: Session = Depends(get_db)):
    """Permite obtener los datos de un curso en especifico.

    Args:
        id (int): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    course = db.query(models.Course).filter_by(id=id).first()

    check_and_raise(
        not course,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found")
    )

    return course


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(
        id: int,
        db: Session = Depends(get_db)):
    """Permite eliminar un curso en especifico.

    Args:
        id (int): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    course = db.query(models.Course).filter_by(id=id).first()

    check_and_raise(
        not course,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found")
    )

    db.delete(course)
    db.commit()

    return "done"


@router.put('/edit/{id}', status_code=status.HTTP_200_OK)
def edit_course(
        id: int,
        request: schemas.course.CourseEdit,
        db: Session = Depends(get_db)):
    """Permite editar un curso en especifico.

    Args:
        id (int): [description]
        request (schemas.course.CourseEdit): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    course = db.query(models.Course).filter_by(id=id).first() # pragma: no cover

    check_and_raise(
        not course,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {id} not found") # pragma: no cover 
    )

    course.name = request.name # pragma: no cover
    course.description = request.description # pragma: no cover

    db.commit() # pragma: no cover

    return {'detail': 'done'} # pragma: no cover
