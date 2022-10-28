from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status,Response
from .. import models,schemas



def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request:schemas.BlogBase,db: Session):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id,response:Response,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no blog available with {id}")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'blog deleted'

def update(id,request:schemas.BlogBase,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no blog available with {id}")
    blog.update({'title':request.title,'body':request.body},synchronize_session='evaluate')
    db.commit()
    return request

def show(id,response:Response,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no blog available with {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND 
        # return {'data':f'no blog available with {id}'}
    return blog
