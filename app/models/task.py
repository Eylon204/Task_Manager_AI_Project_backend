from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str
    due_date: Optional[datetime] = None
    status: str = "pending"
    completed: Optional[bool] = False  # 🔹 משקף את מצב המשימה

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v) 

class TaskCreate(TaskBase):
    estimated_time: Optional[int] = 30
    user_id: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    estimated_time: Optional[int] = None
    completed: Optional[bool] = None  # 🔹 מוסיפים גם בעדכון

class TaskInDB(TaskBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    estimated_time: Optional[int] = 30
    scheduled_time: Optional[datetime] = None