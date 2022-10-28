from typing import Optional,List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from pydantic import BaseModel
import uvicorn
from sqlalchemy.orm import Session

from .hashing import Hash
from . import schemas,models,hashing
from .database import engine,SessionLocal

models.Base.metadata.create_all(engine)

app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/blog',response_model=List[schemas.ShowBlog],tags=['blog'])
def get_all(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog,tags=['blog'])
def show(id,response:Response,db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no blog available with {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND 
        # return {'data':f'no blog available with {id}'}
    return blog


@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blog'])
def create_blog(request:schemas.BlogBase,db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blog'])
def destroy(id,response:Response,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no blog available with {id}")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'blog deleted'

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blog'])
def update(id,request:schemas.BlogBase,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no blog available with {id}")
    blog.update({'title':request.title,'body':request.body},synchronize_session='evaluate')
    db.commit()
    return request



@app.post('/user',response_model=schemas.ShowUsersBase,tags=['user'])
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    new_user = models.User(
        name = request.name,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users',response_model=List[schemas.ShowUsers],tags=['user'])
def get_all(db: Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get('/user/{id}',response_model=schemas.ShowUsers,tags=['user'])
def get_user(id,db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no user available with id {id}")
    return user