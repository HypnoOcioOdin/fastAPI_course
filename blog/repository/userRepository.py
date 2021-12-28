from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi.param_functions import Depends
from starlette import status
from .. import models
from blog.database import get_db
from blog import schemas
from ..hashing import Hash

def create(request: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = Hash.bcrypt(request.password)
    new_user = models.User(name = request.name, email = request.email, password = hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"no user with id {id} found")

    return user