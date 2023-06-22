from pydantic import BaseModel
from typing import Optional
from sqlalchemy import orm


class Data(BaseModel):
    title: str
    body: str


class BlogPost(BaseModel):
    id: int
    title: str
    body: str

    class Config:
        orm_mode = True


class AuthenReq(BaseModel):
    username: str
    password: str


class AuthenRes(BaseModel):
    username: str
    password: str
    id: int


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    title: Optional[str] = None
