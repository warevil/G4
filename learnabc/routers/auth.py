from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models, token
from ..hashing import Hash
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if user.oauth:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This email use Google OAuth!")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/verify_oauth_token')
def verify(request: schemas.auth.TokenOAuth, db: Session = Depends(database.get_db)):
    CLIENT_ID = "204095740277-8khgna7ci9g251auvrsn4mvdrgjgup1i.apps.googleusercontent.com"
    print("request: " + request.token)
    try:
        user_token = request.token
        idinfo = id_token.verify_oauth2_token(
            user_token, requests.Request(), CLIENT_ID)
        us = db.query(models.User).filter_by(email=idinfo["email"]).first()
        if not us:
            us = models.User(
                name=idinfo["name"], email=idinfo["email"], oauth=True)
            db.add(us)
            db.commit()
        access_token = token.create_access_token(data={"sub": us.email})
        return access_token
    except ValueError:
        return "OAuth Error: Invalid Token"
        # return jsonify(success=False)
