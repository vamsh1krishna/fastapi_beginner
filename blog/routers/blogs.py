from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import Optional,List
from sqlalchemy.orm import Session

from ..oauth2 import get_current_user
from .. import schemas,models,database
from .. repository import blog

router = APIRouter(
    prefix = '/blog',
    tags=['Blogs']
)

get_db = database.get_db

@router.get('/',response_model=List[schemas.ShowBlog])
def get_all(db: Session=Depends(get_db),current_user:schemas.User=Depends(get_current_user)):
    return blog.get_all(db)

@router.get('/{id}',status_code=200,response_model=schemas.ShowBlog)
def show(id,response:Response,db: Session=Depends(get_db),current_user:schemas.User=Depends(get_current_user)):
    return blog.show(id,response,db)


@router.post('/',status_code=status.HTTP_201_CREATED)
def create_blog(request:schemas.BlogBase,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_user)):
    return blog.create(request,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int,response:Response,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_user)):
    return blog.destroy(id,response,db)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:int,request:schemas.BlogBase,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_user)):
    return blog.update(id,request,db)
