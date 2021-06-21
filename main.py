from fastapi import FastAPI
from learnabc.routers.user import models
from learnabc.base.database import engine
from learnabc.routers.auth.api import router as auth_router
from learnabc.routers.user.api import router as user_router

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(auth_router)
app.include_router(user_router)
