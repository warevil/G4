from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from learnabc import models
from learnabc.database import engine
from learnabc.routers import course, user, auth

app = FastAPI()

models.Base.metadata.create_all(engine)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(course.router)
app.include_router(user.router)
