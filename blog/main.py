from fastapi import FastAPI, Depends
from . import schemas,models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog')
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    
    # return {"response" : f"we have title -> {request.title}"}
    # return {'title':request.title,"body":request.body}