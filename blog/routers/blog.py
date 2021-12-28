from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from blog import database
from blog.database import get_db
from .. import schemas
from blog import models
from fastapi import status, HTTPException, Response

router = APIRouter(
    prefix="/blog",
    tags=["blocks"]
)

@router.get('/', response_model=List[schemas.ShowBlog] )
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/',status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    # refresh so we can return new_blog
    db.refresh(new_blog)
    return new_blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)    
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"no blog with id {id} found")
    blog.delete(synchronize_session=False)
    db.commit()    
    return {"data": "updated succesfully"}


@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,response: Response, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"no blog with id {id} found")
    blog.update({models.Blog.title: request.title, models.Blog.body: request.body})
    db.commit()    
    return {"data": "updated succesfully"}

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get('/{id}',status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id , response: Response ,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"no blog with id {id} found")

    return blog