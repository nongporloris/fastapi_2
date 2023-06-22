from fastapi import FastAPI, APIRouter, Depends, status, HTTPException
from response_model import BlogPost
from database import engine, SessionLocal, get_db
from starlette import status
import models
from response_model import Data, BlogPost
from sqlalchemy.orm import Session
from typing import List
from oauth import get_current_user

router = APIRouter(
    prefix='/create',
    tags=['Blogs']
)


# models.Base.metadata.create_all(engine)


@router.post('/blog', response_model=BlogPost, status_code=status.HTTP_201_CREATED)
def create(request: Data, db: Session = Depends(get_db), get_current_user: BlogPost = Depends(get_current_user)):
    # title_hash = Hash.get_password_hash(request.title)

    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    # print(type(new_blog.id))
    return {'id': new_blog.id,
            'title': new_blog.title,
            'body': new_blog.body
            }
