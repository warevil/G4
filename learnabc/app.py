from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from learnabc import models
from learnabc.database import engine
from learnabc.routers import comment, course, group, user, auth, publication, submission

"""
Objeto principal de FastAPI
"""
app = FastAPI()

origins = ["*"]

"""
Configuracion de la aplicacion definida para permitirse conexiones desde
cualquier lugar
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Ejecutamos nuestro modelos para crearlos en la base de datos.
"""
models.Base.metadata.create_all(engine)

"""
Incluimos los router de nuestra aplicacion
"""
app.include_router(auth.router)
app.include_router(course.router)
app.include_router(user.router)
app.include_router(publication.router)
app.include_router(submission.router)
app.include_router(comment.router)
app.include_router(group.router)
