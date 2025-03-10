from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument
from app.models.task_model import TaskInDB, TaskCreate, TaskUpdate
from app.core.database import Database
from datetime import datetime
from bson import ObjectId

router = APIRouter()


@router.post("/", response_model=TaskInDB)
async def create_task(task: TaskCreate):
    """יוצר משימה חדשה."""
    db = Database.get_database()

    task_dict = task.dict()
    
    if "id" not in task_dict or not task_dict["id"]:
        task_dict["_id"] = ObjectId()  # יצירת ObjectId אוטומטי

    result = await db["tasks"].insert_one(task_dict)
    
    # הפוך את ה-ObjectId למחרוזת כדי למנוע שגיאת אימות
    task_dict["_id"] = str(result.inserted_id)

    return TaskInDB(**task_dict)

@router.get("/{task_id}", response_model=TaskInDB)
async def get_task(task_id: str):
    """מחזיר משימה לפי ה-ID שלה"""
    db = Database.get_database()

    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    task = await db["tasks"].find_one({"_id": ObjectId(task_id)})

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task["_id"] = str(task["_id"])  # ✅ המרת ObjectId למחרוזת

    return TaskInDB(**task)


@router.put("/{task_id}", response_model=TaskInDB)
async def update_task(task_id: str, task_update: TaskUpdate):
    """מעדכן משימה קיימת לפי ID"""
    db = Database.get_database()

    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    update_data = {k: v for k, v in task_update.dict(exclude_unset=True).items()}

    updated_task = await db["tasks"].find_one_and_update(
        {"_id": ObjectId(task_id)}, 
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task["id"] = str(updated_task["_id"])
    updated_task.pop("_id", None)  # מסירים את `_id` מהתשובה

    print(f"🔄 Updated task: {updated_task}")
    return TaskInDB(**updated_task)


@router.delete("/{task_id}", status_code=200)
async def delete_task(task_id: str):
    """מוחק משימה לפי מזהה"""
    db = Database.get_database()

    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    result = await db["tasks"].delete_one({"_id": ObjectId(task_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    print(f"🗑 Task {task_id} deleted successfully")
    return {"message": "Task deleted successfully"}


@router.get("/", response_model=list[TaskInDB])
async def get_all_tasks():
    """מחזיר את כל המשימות"""
    db = Database.get_database()
    tasks_cursor = db["tasks"].find()
    tasks = await tasks_cursor.to_list(length=None)

    for task in tasks:
        task["_id"] = str(task["_id"])  # ✅ המרה למחרוזת

    return tasks