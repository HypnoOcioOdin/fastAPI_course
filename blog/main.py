from os import name
from typing import List
from fastapi import FastAPI, Depends,status, Response, HTTPException
from sqlalchemy.sql.expression import null
from . import schemas,models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from .hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED, tags=["blocks"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    # refresh so we can return new_blog
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=["blocks"])    
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"no blog with id {id} found")
    blog.delete(synchronize_session=False)
    db.commit()    
    return {"data": "updated succesfully"}


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, tags=["blocks"])
def update(id,response: Response, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"no blog with id {id} found")
    blog.update({models.Blog.title: request.title, models.Blog.body: request.body})
    db.commit()    
    return {"data": "updated succesfully"}

@app.get('/blog', response_model=List[schemas.ShowBlog], tags=["blocks"])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}',status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["blocks"])
def show(id , response: Response ,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"no blog with id {id} found")

    return blog




@app.post('/user',status_code=status.HTTP_201_CREATED, tags=["users"])
def create(request: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = Hash.bcrypt(request.password)
    new_user = models.User(name = request.name, email = request.email, password = hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#, response_model=schemas.ShowUser
@app.get('/user/{id}',status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["users"])
def show(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"no user with id {id} found")

    return user