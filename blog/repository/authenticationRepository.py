
from datetime import timedelta
from fastapi.param_functions import Depends
from starlette import status
from blog import schemas
from blog.JWTtoken import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from ..database import get_db
from ..models import User
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from ..hashing import Hash
from .. import JWTtoken
   

def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                            detail = f"no user with name {request.email} found")
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,\
                            detail = f"wrong password provided")

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": user.username}, expires_delta=access_token_expires
    # )
    access_token = JWTtoken.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
