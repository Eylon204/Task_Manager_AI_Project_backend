from fastapi import APIRouter, HTTPException
from app.models.task_model import TaskInDB
from app.core.database import Database
from app.ai.scheduler import schedule_tasks
from typing import List
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()
executor = ThreadPoolExecutor()

@router.get("/optimize", response_model=List[TaskInDB])
async def optimize_schedule():
    db = Database.db
    tasks_raw = await db.tasks.find().to_list(None)  # טוען את כל המשימות
    
    if not tasks_raw:
        raise HTTPException(status_code=404, detail="No tasks found")
    
    # המרה של הנתונים ממונגו ל-TaskInDB
    tasks = [TaskInDB(**task) for task in tasks_raw]
    
    # הפעלת תכנון המשימות ב-ThreadPool כדי למנוע חסימה של השרת
    loop = asyncio.get_running_loop()
    optimized_tasks = await loop.run_in_executor(executor, schedule_tasks, tasks)
    
    return optimized_tasks
