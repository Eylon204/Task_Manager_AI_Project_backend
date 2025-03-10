from pydantic import BaseModel, Field
from typing import Optional

class EventBase(BaseModel):
    """Base model for an event"""
    title: str = Field(..., title="Event Title", example="Team Meeting")
    description: Optional[str] = None
    location: Optional[str] = None
    date: str = Field(..., title="Event Date (ISO format)", example="2024-02-10T14:00:00")  # ✅ שומר את התאריך כמחרוזת
    user_id: str

class EventCreate(EventBase):
    """Model for creating a new event"""
    pass

class EventUpdate(BaseModel):
    """Model for updating an existing event"""
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date: Optional[str] = None  # ✅ ווידוא שהתאריך נשמר כמחרוזת

class EventInDB(EventBase):
    """Model for storing an event in the database"""
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True 