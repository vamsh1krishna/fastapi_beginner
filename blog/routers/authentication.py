from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from ..hashing import Hash
from ..database import get_db
from .. import schemas,models

router = APIRouter(
    tags = ["Authentication"]
)

@router.post('/login')
def login(request:schemas.Login,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no user available with username {request.username}")
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")
    # Generate JWT token if password verified
    return 'login'