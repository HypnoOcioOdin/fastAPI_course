from os import name
from fastapi import FastAPI
from . import models
from .database import engine
from blog.routers import blog
from blog.routers import user


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)
