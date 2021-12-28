from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from blog.database import get_db
from .. import schemas
from fastapi import status
from blog.repository import blogRepository
router = APIRouter(
    prefix="/blog",
    tags=["blocks"]
)

@router.get('/', response_model=List[schemas.ShowBlog] )
def all(db: Session = Depends(get_db)):
    return blogRepository.get_all(db)

@router.post('/',status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blogRepository.create(request,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)    
def destroy(id:int, db: Session = Depends(get_db)):
    return blogRepository.destroy(id,db)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blogRepository.update(id,request,db)

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return blogRepository.all(db)


@router.get('/{id}',status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id:int , db: Session = Depends(get_db)):
    return blogRepository.show(id,db)