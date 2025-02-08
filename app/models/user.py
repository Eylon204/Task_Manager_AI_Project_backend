from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    """Base user model."""
    username: str
    email: str

class UserCreate(UserBase):
    """Model for user creation."""
    password: str  # Ensure passwords are hashed before storing

class UserUpdate(BaseModel):
    """Model for user updates."""
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    """User model stored in the database."""
    id: str