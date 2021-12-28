from fastapi import APIRouter
from fastapi.param_functions import Depends
from blog import schemas
from ..database import get_db
from ..repository import authenticationRepository
from sqlalchemy.orm import Session


router = APIRouter(
    tags = ["authentication"]
)

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    return authenticationRepository.login(request,db)
    