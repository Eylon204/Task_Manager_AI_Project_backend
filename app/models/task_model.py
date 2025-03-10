from pydantic import BaseModel, Field
from typing import Optional, Literal
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class TaskBase(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # המרת _id ל-id
    title: str
    description: Optional[str] = None
    priority: Literal["low", "medium", "high"]
    due_date: Optional[str] = None  # תאריך בפורמט ISO
    status: Literal["pending", "completed"] = "pending"
    completed: Optional[bool] = False

    class Config:
        populate_by_name = True  # מוודא גישה נכונה לשדות
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class TaskCreate(TaskBase):
    estimated_time: Optional[int] = 30
    user_id: str
    scheduled_time: Optional[str] = None  # לוודא שמתווסף ליצירת משימות חדשות

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    due_date: Optional[str] = None
    status: Optional[Literal["pending", "completed"]] = None
    estimated_time: Optional[int] = None
    scheduled_time: Optional[str] = None
    completed: Optional[bool] = None

class TaskInDB(TaskBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    estimated_time: Optional[int] = 30
    scheduled_time: Optional[str] = None