from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument
from app.models.task import TaskInDB, TaskCreate, TaskUpdate
from app.core.database import Database
from datetime import datetime
from bson import ObjectId

router = APIRouter()

from bson import ObjectId

@router.post("/", response_model=TaskInDB)
async def create_task(task: TaskCreate):
    """יוצר משימה חדשה וממיר את ה-ObjectId ל-string"""
    db = Database.get_database()
    task_dict = task.dict()
    
    # הכנס למסד הנתונים
    result = await db["tasks"].insert_one(task_dict)

    # המרת ObjectId למחרוזת לפני ההחזרה
    task_dict["_id"] = str(result.inserted_id)

    return TaskInDB(**task_dict)

@router.get("/{task_id}", response_model=TaskInDB)
async def get_task(task_id: str):
    """Returns a task by its custom ID"""
    db = Database.get_database()

    task = await db["tasks"].find_one({"_id": ObjectId(task_id)}) 

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task["id"] = str(task["_id"])  
    task.pop("_id", None)  
    task["completed"] = task["status"] == "completed"

    return TaskInDB(**task)

@router.put("/{task_id}", response_model=TaskInDB)
async def update_task(task_id: str, task_update: TaskUpdate):
    """Updates an existing task by its ID (_id)"""
    db = Database.get_database()

    try:
        obj_id = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    update_data = {k: v for k, v in task_update.model_dump().items() if v is not None}
    print(f"🔄 Updating task {task_id} with data:", update_data)

    updated_task = await db["tasks"].find_one_and_update(
        {"_id": obj_id}, 
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )

    if not updated_task:
        print(f"❌ Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task["id"] = str(updated_task["_id"])
    updated_task.pop("_id", None)
    updated_task["completed"] = updated_task["status"] == "completed"

    if "due_date" in updated_task and isinstance(updated_task["due_date"], datetime):
        updated_task["due_date"] = updated_task["due_date"].isoformat()

    print("✅ Updated task:", updated_task)
    return TaskInDB(**updated_task)

@router.delete("/{task_id}", status_code=200)
async def delete_task(task_id: str):
    """Deletes a task by its ID (_id)."""
    db = Database.get_database()

    try:
        obj_id = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    result = await db["tasks"].delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    print(f"✅ Task {task_id} deleted successfully from database")
    return {"message": "Task deleted successfully"}

@router.get("/", response_model=list[TaskInDB])
async def get_all_tasks():
    """Returns all tasks from the server"""
    db = Database.get_database()
    tasks_cursor = db["tasks"].find()
    tasks = await tasks_cursor.to_list(length=None)

    for task in tasks:
        task["id"] = str(task["_id"]) 
        task.pop("_id", None)  
        task["completed"] = task["status"] == "completed"

    print("✅ Returning tasks with IDs:", tasks)
    return tasks