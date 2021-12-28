from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from blog.database import get_db
from .. import schemas
from fastapi import status
from blog.repository import userRepository

router = APIRouter(
    prefix = "/user",
    tags=["users"]
)

@router.post('/',status_code=status.HTTP_201_CREATED, )
def create(request: schemas.User, db: Session = Depends(get_db)):
    return userRepository.create(request,db)

#, response_model=schemas.ShowUser
@router.get('/{id}',status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def show(id: int, db: Session = Depends(get_db)):
    return userRepository.show(id,db)