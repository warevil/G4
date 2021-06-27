from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from learnabc import models
from learnabc.database import engine
from learnabc.routers import course, user, auth, publication, submission

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(course.router)
app.include_router(user.router)
app.include_router(publication.router)
app.include_router(submission.router)
