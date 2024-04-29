from fastapi import FastAPI, Response, status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
from .. database import engine, get_db
from typing import List

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts'] # helps to group every route in this router together in documentation
    
)

@router.get('/', response_model = List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post('/',status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content,post.published))
    # post = cursor.fetchone()
    # conn.commit()
    post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/{id}", response_model = schemas.Post)
def get_post(id : int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =  f"post with id {id} was not found" )
    return post

@router.delete('/{id}',status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts where id = %s RETURNING *""",(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post:
        if post.owner_id != current_user.id:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =  f"post with id {id} was not found" )

@router.put("/{id}", response_model = schemas.Post)
def update_post(id : int, post : schemas.PostCreate,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_instance = post_query.first()
    if post_instance:
        if post_instance.owner_id != current_user.id:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        post_query.update(post.model_dump(),synchronize_session=False)
        db.commit()
        return post_query.first()
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =  f"post with id {id} was not found" )