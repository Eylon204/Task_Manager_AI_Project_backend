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

class TaskInDB(TaskBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    estimated_time: Optional[int] = 30
    scheduled_time: Optional[datetime] = None  # Added scheduled_time field