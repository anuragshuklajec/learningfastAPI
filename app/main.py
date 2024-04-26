import logging
from fastapi import FastAPI, Response, status,HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from typing import List
from .routers import user,post

logging.getLogger('passlib').setLevel(logging.ERROR) #supressing a warning that bycrypt raise with newer versions and has nothing to do with logic

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='root',cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("db connection succesfull")
        break
    except Exception as e:
        print("connection to database failed")
        print("Error : ", e)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)

@app.get('/')
def root():
    return {"message" : "welcome to my api"}




