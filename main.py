from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from starlette import status
from response_model import Data, BlogPost
from database import engine, get_db
import models
from sqlalchemy.orm import Session
from typing import List
from routers import functionroute, authentication
from query import queryall
from oauth import get_current_user

app = FastAPI()

models.Base.metadata.create_all(engine)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# add new user to database
# @app.post('/blog', response_model=BlogPost, status_code=status.HTTP_201_CREATED)
# def create(request: Data, db: Session = Depends(get_db)):
#
#     # title_hash = Hash.get_password_hash(request.title)
#
#     new_blog = models.Blog(title=request.title, body=request.body)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#
#     # print(type(new_blog.id))
#     return {'id': new_blog.id,
#             'title': new_blog.title,
#             'body': new_blog.body
#             }


# query all data in database
# @app.get('/queryall', response_model=List[BlogPost])
# def all(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


# select specific data compare with id
@app.get('/selected/{id}')
def all( id = int, db: Session = Depends(get_db), get_current_user: BlogPost = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).all()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the {id} is not available ')
    return blog


# delete form selected id
@app.delete('/delete/{id}')
def nomore(id, db: Session = Depends(get_db), get_current_user: BlogPost = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)

    db.commit()

    return db.query(models.Blog).all()


@app.put('/putting/{id}', response_model=BlogPost)
def update(request: Data, id, db: Session = Depends(get_db), get_current_user: BlogPost = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).update({'title': request.title,
                                                                      'body': request.body})

    if blog == 1:
        db.commit()
        return db.query(models.Blog).filter(models.Blog.id == id).first()
    elif blog == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No {id} in the database')


app.include_router(functionroute.router)
app.include_router(queryall.router)
app.include_router(authentication.router)
