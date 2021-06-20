from fastapi import FastAPI
from learnabc import models
from learnabc.database import engine
from learnabc.routers import learnabc, user, auth

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(learnabc.router)
app.include_router(user.router)
