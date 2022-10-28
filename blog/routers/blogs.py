from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import Optional,List
from sqlalchemy.orm import Session

from .. import schemas,models,database

router = APIRouter(
    prefix = '/blog',
    tags=['Blogs']
)

get_db = database.get_db

@router.get('/',response_model=List[schemas.ShowBlog])
def get_all(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get('/{id}',status_code=200,response_model=schemas.ShowBlog)
def show(id,response:Response,db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no blog available with {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND 
        # return {'data':f'no blog available with {id}'}
    return blog


@router.post('/',status_code=status.HTTP_201_CREATED)
def create_blog(request:schemas.BlogBase,db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,response:Response,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no blog available with {id}")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'blog deleted'

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.BlogBase,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no blog available with {id}")
    blog.update({'title':request.title,'body':request.body},synchronize_session='evaluate')
    db.commit()
    return request
