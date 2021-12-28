# to get a string like this run:
# openssl rand -hex 32
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
SECRET_KEY = "2ca8200023f83de46ca66087fb1adfa9ef27daa95a325d503d29ffb908d2ff2a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt