from fastapi import APIRouter,Depends
from typing import Optional,List
from sqlalchemy.orm import Session

from .. import schemas,database
from ..repository import user

router = APIRouter(
    prefix = '/user',
    tags=['User']
)

get_db = database.get_db

@router.post('/',response_model=schemas.ShowUsersBase)
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    return user.create(request,db)

@router.get('/',response_model=List[schemas.ShowUsers])
def get_all(db: Session=Depends(get_db)):
    return user.get_all(db)

@router.get('/{id}',response_model=schemas.ShowUsers)
def get_user(id:int,db: Session=Depends(get_db)):
    return user.get_user(id,db)