# backend/app/routes/ai.py
from fastapi import APIRouter, HTTPException
from app.models.task import TaskInDB
from app.core.database import Database
from app.ai.scheduler import schedule_tasks
from typing import List

router = APIRouter()

@router.get("/optimize", response_model=List[TaskInDB])
async def optimize_schedule():
    db = Database.db
    tasks = await db.tasks.find().to_list(100)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    
    optimized_tasks = schedule_tasks(tasks)
    return optimized_tasks
