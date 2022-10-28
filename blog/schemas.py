from pydantic import BaseModel
from typing import Optional,List

class BlogBase(BaseModel):
    title:str
    body:str
    user_id : int


class Blog(BlogBase):
    title:str
    body:str
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email : str
    password : str


class ShowUsersBase(BaseModel):
    name: str
    email : str
    class Config:
        orm_mode = True

class ShowUsers(ShowUsersBase):
    name: str
    email : str
    blogs : List[Blog]
    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    title : str
    body : str
    creator : ShowUsersBase
    class Config:
        orm_mode = True
