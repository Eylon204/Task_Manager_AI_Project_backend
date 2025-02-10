from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    """Base model for an event"""
    title: str = Field(..., title="Event Title", example="Team Meeting")
    description: Optional[str] = Field(None, title="Event Description", example="Project discussion")
    location: Optional[str] = Field(None, title="Event Location", example="Office")
    date: datetime = Field(..., title="Event Date", example="2024-02-10T14:00:00")
    user_id: str = Field(..., title="User ID", example="67a7a02ba661889e66344951")

class EventCreate(EventBase):
    """Model for creating a new event"""
    pass

class EventUpdate(EventBase):
    """Model for updating an existing event"""
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date: Optional[datetime] = None

class EventInDB(EventBase):
    """Model for storing an event in the database"""
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True 
        from_attributes = True  