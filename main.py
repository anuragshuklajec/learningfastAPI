from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get('/')
def root():
    return {"message" : "welcome to my api"}


@app.get('/posts')
def get_post():
    return {"data" : "this is your post"};

@app.post('/createposts')
def create_post(payload : dict = Body(...)):
    print(payload)
    return  {"new_post" : f" title : {payload['title']} content : {payload['title']}"}
