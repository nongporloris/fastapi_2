from fastapi import APIRouter, Depends, HTTPException
from database import get_db
import models
from sqlalchemy.orm import Session
from typing import List
from response_model import BlogPost
from oauth import get_current_user

router = APIRouter(
    prefix='/query',
    tags=['Query']
)


@router.get('/queryall', response_model=List[BlogPost])
def all(db: Session = Depends(get_db), get_current_user: BlogPost = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs
