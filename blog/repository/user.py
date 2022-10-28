from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status,Response

from ..hashing import Hash
from .. import models,schemas

def create(request:schemas.User,db:Session):
    new_user = models.User(
        name = request.name,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all(db: Session):
    users = db.query(models.User).all()
    return users

def get_user(id,db: Session):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no user available with id {id}")
    return user