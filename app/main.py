import logging
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user,post,auth
from .config import settings

logging.getLogger('passlib').setLevel(logging.ERROR) #supressing a warning that bycrypt raise with newer versions and has nothing to do with logic

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {"message" : "welcome to my api"}




