from fastapi import APIRouter, HTTPException
from app.core.database import Database
from bson import ObjectId
from typing import List
from datetime import datetime

router = APIRouter(tags=["calendar"])

@router.get("/", response_model=List[dict])
async def get_calendar_items():
    db = Database.get_database()

    # Get tasks
    tasks = await db["tasks"].find().to_list(length=None)
    events = await db["events"].find().to_list(length=None)

    calendar_items = []
    for task in tasks:
        calendar_items.append({
            "id": str(task["_id"]),
            "title": task["title"],
            "start": task.get("scheduled_time", datetime.utcnow().isoformat()),
            "type": "task",
            "color": "#ffcc00"
        })

    for event in events:
        calendar_items.append({
            "id": str(event["_id"]),
            "title": event["title"],
            "start": event["date"],
            "type": "event",
            "color": "#007bff"
        })

    return calendar_items

@router.get("/check-conflicts/{user_id}")
async def check_conflicts(user_id: str):
    db = Database.get_database()
    
    # Get all tasks and events for user:
    tasks = await db["tasks"].find({"user_id": user_id}).to_list(length=None)
    events = await db["events"].find({"user_id": user_id}).to_list(length=None)

    conflicts = []

    for task in tasks:
        for event in events:
            if task.get("scheduled_time") and event.get("date"):
                task_time = datetime.fromisoformat(task["scheduled_time"])
                event_time = datetime.fromisoformat(event["date"])

                if task_time.date() == event_time.date():
                    conflicts.append({
                        "task_id": str(task["_id"]),
                        "event_id": str(event["_id"]),
                        "task_title": task["title"],
                        "event_title": event["title"]
                    })
    return {"conflicts": conflicts}