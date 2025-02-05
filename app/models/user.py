from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    hashed_password: str
    is_active: bool = True

class UserInDB(UserBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserPublic(UserBase):
    ID: str