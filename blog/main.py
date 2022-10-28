from typing import List
from fastapi import FastAPI

from . import models
from .routers.blogs import router as blog_router
from .routers.users import router as user_router
from .database import engine

models.Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(blog_router)
app.include_router(user_router)