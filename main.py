from fastapi import FastAPI
#from learnabc import models
from learnabc.database import engine
from learnabc.routers.course import api as course,models
from learnabc.routers.user import api as user,models
from learnabc.routers.auth import api as auth,models

app = FastAPI()

models.Base.metadata.create_all(engine)
app.include_router(auth.router)
app.include_router(course.router)
app.include_router(user.router)
