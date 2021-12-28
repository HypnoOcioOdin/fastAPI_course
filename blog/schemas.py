from pydantic import BaseModel
from typing import List, Optional

class BaseBlog(BaseModel):
    title: str
    body: str

class Blog(BaseBlog):
    class Config():
        orm_mode = True

class User(BaseModel):    
    name:str
    email: str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config():
        orm_mode = True


class BaseLogin(BaseModel):
    email: str
    password: str

class Login(BaseLogin):
    class Config():
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None