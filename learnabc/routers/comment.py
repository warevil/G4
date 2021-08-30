from hashlib import new
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import false
from .. import database, models, oauth2, schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/comment",
    tags=['Comment']
)

get_db = database.get_db


@router.post('/{comment_id}', status_code=status.HTTP_201_CREATED)
def post_subcomment(
        comment_id: int,
        request: schemas.comment.RequestComment,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):
    """Permite crear un nuevo comentario.

    Args:
        comment_id (int): [description]
        request (schemas.comment.RequestComment): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).
        current_user (schemas.base.User, optional): [description]. Defaults to Depends(oauth2.get_current_user).

    Returns:
        [type]: [description]
    """
    new_comment = models.Comment(  # pragma: no cover
        content=request.content,
        user_id=current_user.id,
        parent_id=comment_id
    )

    db.add(new_comment)  # pragma: no cover
    db.commit()  # pragma: no cover

    return "done"  # pragma: no cover


@router.post('/{comment_id}/reaction/{type}', status_code=status.HTTP_201_CREATED)
def post_comment_reaction(
        comment_id: int,
        type: int,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):
    """Permite postear una reaccion a algun comentario.

    Args:
        comment_id (int): [description]
        type (int): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).
        current_user (schemas.base.User, optional): [description]. Defaults to Depends(oauth2.get_current_user).

    Returns:
        [type]: [description]
    """
    new_comment_reaction = models.CommentReaction(  # pragma: no cover
        user_id=current_user.id,
        comment_id=comment_id,
        type=type
    )

    db.add(new_comment_reaction)  # pragma: no cover
    db.commit()  # pragma: no cover

    return "done"  # pragma: no cover


@router.get('/publication/{publication_id}', response_model=List[schemas.comment.ShowCommentPublication], status_code=status.HTTP_201_CREATED)
def get_publication_comments(publication_id: int, db: Session = Depends(get_db)):
    """Permite obtener todos los comentarios de una publicacion en particular.

    Args:
        publication_id (int): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Returns:
        [type]: [description]
    """
    return db.query(models.Comment).filter_by(publication_id=publication_id).all()

@router.get('/sub/{comment_id}', response_model=List[schemas.comment.SubComment], status_code=status.HTTP_201_CREATED)
def get_subcomments(comment_id: int, db: Session = Depends(get_db)):
    """Permite obtener todos los subcomentarios de un comentario en especifico.

    Returns:
        [type]: [description]
    """
    return db.query(models.Comment).filter_by(parent_id=comment_id).all()
