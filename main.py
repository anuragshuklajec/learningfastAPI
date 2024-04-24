from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True #default value partially optional
    rating : Optional[int] = None
    

@app.get('/')
def root():
    return {"message" : "welcome to my api"}


@app.get('/posts')
def get_post():
    return {"data" : "this is your post"};

@app.post('/posts')
def create_post(post : Post):
    print(post)
    return  {"data" : post}
