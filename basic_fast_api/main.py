from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/blog')
def index(limit=10,published:bool=True,sort:Optional[str]=None):
    if published:
        return {'data':f'{limit} published blogs from db'}
    else :
        return {'data':f'{limit} blogs from db'}

class Blog(BaseModel):
    title : str
    body :str
    published : Optional[bool]

@app.post('/blog')
def create_blog(blog:Blog):
    return {'data': f"succesfully created blog with title {blog.title}"}

@app.get('/about')
def about():
    return {'data':{'loc':'about_page'}}

@app.get('/blog/unpublished')
def unpublished():
    return {'data':'all unpublished data'}

@app.get('/blog/{id}')
def show(id:int):
    """fetch blog with id """
    return {'data': id}

@app.get('/blog/{id}/comments')
def comments(id:str):
    """fetch comments of blog with id"""
    return {'data' : {'id':id,'comments': [1,2]}}