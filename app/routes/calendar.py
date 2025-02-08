from fastapi import APIRouter, HTTPException
from app.core.database import Database
from app.models.task import TaskInDB
from app.services.calendar_service import sync_with_google_calendar
from typing import List

router = APIRouter()

# func for Sync Calendar:
async def sync_calendar():
    db = Database.db
    tasks = await db.tasks.find().to_list(100)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found to sync")
    
    synced_tasks = sync_with_google_calendar(tasks)
    return synced_tasks