
from fastapi.param_functions import Depends
from starlette import status
from blog import schemas
from ..database import get_db
from ..models import User
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from ..hashing import Hash
   

def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"no user with name {request.email} found")
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"wrong password provided")

    # generate JWT token and return it
    return user