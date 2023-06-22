from fastapi import APIRouter, Depends, HTTPException

import database
from response_model import AuthenRes, AuthenReq,TokenModel
from database import engine, get_db
from sqlalchemy.orm import Session
from starlette import status
import models
from tokenmaker import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/authen',
    tags=['Login']
)


@router.post('/login', response_model=TokenModel)
def login(request: AuthenReq, db: Session = Depends(database.get_db)):
    user = db.query(models.Blog).filter(models.Blog.title == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No {id} in the database')

    access_token = create_access_token(data={"sub":user.title})

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }
