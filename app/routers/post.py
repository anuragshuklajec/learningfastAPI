from fastapi import FastAPI, Response, status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from .. database import engine, get_db
from typing import List

router = APIRouter()

@router.get('/posts', response_model = List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post('/posts',status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content,post.published))
    # post = cursor.fetchone()
    # conn.commit()
    post = models.Post(**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/posts/{id}", response_model = schemas.Post)
def get_post(id : int,db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =  f"post with id {id} was not found" )
    return post

@router.delete('/posts/{id}',status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts where id = %s RETURNING *""",(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =  f"post with id {id} was not found" )

@router.put("/posts/{id}", response_model = schemas.Post)
def update_post(id : int, post : schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first():
        post_query.update(post.model_dump(),synchronize_session=False)
        db.commit()
        return post_query.first()
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =  f"post with id {id} was not found" )