from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi.param_functions import Depends
from starlette import status
from .. import models
from blog.database import get_db
from blog import schemas


def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    # refresh so we can return new_blog
    db.refresh(new_blog)
    return new_blog

def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"no blog with id {id} found")
    blog.delete(synchronize_session=False)
    db.commit()    
    return {"data": "updated succesfully"}

def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"no blog with id {id} found")
    blog.update({models.Blog.title: request.title, models.Blog.body: request.body})
    db.commit()    
    return {"data": "updated succesfully"}

def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

def show(id:int , db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"no blog with id {id} found")

    return blog