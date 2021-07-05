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

    new_comment = models.Comment(
        content=request.content,
        user_id=current_user.id,
        parent_id=comment_id
    )

    db.add(new_comment)
    db.commit()

    return "done"


@router.post('/{comment_id}/reaction/{type}', status_code=status.HTTP_201_CREATED)
def post_comment_reaction(
        comment_id: int,
        type: int,
        db: Session = Depends(get_db),
        current_user: schemas.base.User = Depends(oauth2.get_current_user)):

    new_comment_reaction = models.CommentReaction(
        user_id=current_user.id,
        comment_id=comment_id,
        type=type
    )

    db.add(new_comment_reaction)
    db.commit()

    return "done"


@router.get('/publication/{publication_id}', response_model=List[schemas.comment.ShowCommentPublication], status_code=status.HTTP_201_CREATED)
def get_publication_comments(publication_id: int, db: Session = Depends(get_db)):
    return db.query(models.Comment).filter_by(publication_id=publication_id).all()


@router.get('/sub/{comment_id}', response_model=List[schemas.comment.SubComment], status_code=status.HTTP_201_CREATED)
def get_subcomments(comment_id: int, db: Session = Depends(get_db)):
    return db.query(models.Comment).filter_by(parent_id=comment_id).all()
