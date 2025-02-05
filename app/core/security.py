from datetime import datetime, timedelta
from typing import Union
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hased_password: str) -> bool:
    return pwd_context.verify(plain_password, hased_password)

# JWT Token handling
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta 
    else:
        expire = datetime.utcnow() + timedelta (minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp":expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt