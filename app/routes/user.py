# backend/app/routes/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserCreate, UserPublic, UserInDB
from app.core.security import hash_password, verify_password, create_access_token
from app.core.database import Database
from pymongo.errors import DuplicateKeyError
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserPublic)
async def register_user(user: UserCreate):
    db = Database.db
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    new_user = UserInDB(name=user.name, email=user.email, hashed_password=hashed_password)
    await db.users.insert_one(new_user.dict(by_alias=True))
    return UserPublic(**new_user.dict())

@router.post("/login")
async def login_user(user: UserCreate):
    db = Database.db
    existing_user = await db.users.find_one({"email": user.email})
    if not existing_user or not verify_password(user.password, existing_user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
