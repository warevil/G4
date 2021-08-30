from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models, token
from ..hashing import Hash
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter(tags=['Authentication'])

"""
Permite logear a un usuario pero no es valido para login con Google, sino
para usuario con usuario y contraseña
"""
@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if user.oauth:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"This email use Google OAuth!")  # pragma: no cover
                            
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


""" 
Permite logear a un usuario como superuser con cualquier otro usuario,
este metodo es muy inseguro para la aplicacion y debe eliminarse 
pronto.
"""
@router.post('/login/{email}/{key}')
def private_login(email: str, key: str, db: Session = Depends(database.get_db)):
    access_token = token.create_access_token(data={"sub": email})  # pragma: no cover
    if (key == 'superadmin'):  # pragma: no cover
        return {"access_token": access_token, "token_type": "bearer"}  # pragma: no cover


""" 
Este método permite logear a un usuario mediante el login de Google,
por lo cual recibe un token el cual es validado para así validar
el logeo de Google. 
"""
@router.post('/verify_oauth_token')
def verify(request: schemas.auth.TokenOAuth, db: Session = Depends(database.get_db)):
    CLIENT_ID = "204095740277-8khgna7ci9g251auvrsn4mvdrgjgup1i.apps.googleusercontent.com" # pragma: no cover
    try: # pragma: no cover
        user_token = request.token # pragma: no cover
        idinfo = id_token.verify_oauth2_token( # pragma: no cover
            user_token, requests.Request(), CLIENT_ID) # pragma: no cover
        us = db.query(models.User).filter_by(email=idinfo["email"]).first() # pragma: no cover
        if not us: # pragma: no cover
            us = models.User( # pragma: no cover
                name=idinfo["name"], email=idinfo["email"], oauth=True) # pragma: no cover
            db.add(us) # pragma: no cover
            db.commit() # pragma: no cover
        access_token = token.create_access_token(data={"sub": us.email}) # pragma: no cover
        return access_token # pragma: no cover
    except ValueError: # pragma: no cover
        return "OAuth Error: Invalid Token" # pragma: no cover
