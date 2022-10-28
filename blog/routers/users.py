from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import Optional,List
from sqlalchemy.orm import Session

from .. import schemas,models,database
from ..hashing import Hash

router = APIRouter(
    prefix = '/user',
    tags=['User']
)

get_db = database.get_db

@router.post('/',response_model=schemas.ShowUsersBase)
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

@router.get('/',response_model=List[schemas.ShowUsers])
def get_all(db: Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/{id}',response_model=schemas.ShowUsers)
def get_user(id,db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no user available with id {id}")
    return user