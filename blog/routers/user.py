from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from blog import database
from blog.database import get_db
from .. import schemas
from blog import models
from fastapi import status, HTTPException, Response
from blog.hashing import Hash


router = APIRouter()

@router.post('/user',status_code=status.HTTP_201_CREATED, tags=["users"])
def create(request: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = Hash.bcrypt(request.password)
    new_user = models.User(name = request.name, email = request.email, password = hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#, response_model=schemas.ShowUser
@router.get('/user/{id}',status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["users"])
def show(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"no user with id {id} found")

    return user