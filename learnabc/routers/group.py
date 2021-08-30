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

"""
Permite crear un grupo en un curso en espeficico que es quien tenga como id a
course_id, se le indica el nombre del grupo mediante el parametro 'name'.
Si el nombre es 'default se asignará un nombre con el número de grupo que es
segun la cantidad de grupos que haya ya creados en ese curso.
"""
@router.post('/create/{course_id}/{name}', status_code=status.HTTP_201_CREATED)
def create_group(course_id: int, name: str, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=course_id).first()
    if name == 'default':
        name = 'Grupo ' + str(len(course.groups)+1)
    new_group = models.Group(name=name, course_id=course_id)
    db.add(new_group)
    db.commit()
    return new_group.id

"""
Permite unirse a un grupo al usuario actual, para eso se requiere que el usuario
esté logeado, y se requiere que se pase el id del grupo por parametro en la url
para esto se requiere que el grupo no esté bloqueado
"""
@router.post('/join_me/{id}', status_code=status.HTTP_200_OK)
def join_me(
        id: int,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    group = db.query(models.Group).filter_by(id=id).first()

    if group.locked:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail='the group has been lock')

    inscription = db.query(models.Inscription).filter_by(
        course_id=group.course.id,
        user_id=current_user.id
    ).first()

    inscription.group = group
    db.commit()
    return 'done'

"""
Permite unir a un grupo a un usuario donde se debe indicar o el id del usuaio o su email
para unirlo al grupo con id el cual se pase por parametro en la url.
"""
@router.post('/join/{id}', status_code=status.HTTP_200_OK)
def join(id: int, request: schemas.group.RequestJoin, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter_by(id=id).first()

    if group.locked:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail='the group has been lock')

    if (request.user_email):
        user = db.query(models.User).filter_by(
            email=request.user_email).first()
    else:
        user = db.query(models.User).filter_by(id=request.user_id).first() # pragma: no cover

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail='user does not exist')

    inscription = db.query(models.Inscription).filter_by(
        user_id=user.id,
        course_id=group.course.id
    ).first()

    inscription.group = group
    db.commit()

    return 'done'

"""
Permite bloquear un grupo el cual tenga el id que se indique por parametro
en la url
"""
@router.put('/lock/{id}')
def lock_group(id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter_by(id=id).first()
    group.locked = True
    db.commit()
    return 'done'

"""
Bloquea todos los grupos que pertenezcan a un grupo el cual se indique por parametro
en la url
"""
@router.put('/lock_all/{course_id}')
def lock_group(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=course_id).first()
    for g in course.groups:
        g.locked = True
    db.commit()
    return 'done'

"""
Permite obtener todos los grupos de un curso en espeficico el cual se indique por
parametro en la url
"""
@router.get('/{course_id}', response_model=List[schemas.base.Group])
def get_course_groups(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter_by(id=course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail='course does not exist')
    return course.groups

"""
Permite obetener todos las inscriptions que tiene un grupo en espeficico el
cual se indique por parametro en la url.
"""
@router.get('/inscriptions/{group_id}', response_model=List[schemas.base.GroupInscriptons])
def get_inscriptions(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter_by(id=group_id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail='group does not exist')
    return group.inscriptions

"""
Permite eliminar un grupo el cual se indique por parametro en la url.
"""
@router.delete('/{group_id}')
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter_by(id=group_id).first()
    if not group:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, # pragma: no cover
                            detail='group does not exist')
    db.delete(group)
    db.commit()
    return {'detail': 'done'}
