from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    priority: str = Field(...,regex="^(low|medium|high)$")
    due_date: Optional[datetime] = None
    status: str = Field(default="pending", regex="^(pending|completed|cancelled)$")

class TaskInDB(TaskBase):
    id: str = Field(default_factory=lambda: str(ObjectId()),alias="_id")
    user_id: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority:Optional[str] = None
    due_date:Optional[datetime] = None
    status: Optional[str] = None