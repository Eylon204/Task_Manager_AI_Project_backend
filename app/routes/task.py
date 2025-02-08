from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument
from app.models.task import TaskInDB, TaskCreate, TaskUpdate
from app.core.database import Database
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=TaskInDB, status_code=201)
async def create_task(task: TaskCreate):
    """Creates a new task."""
    task_dict = task.model_dump()
    task_dict["_id"] = ObjectId()  # יצירת מזהה MongoDB תקין
    db = Database.get_database()
    await db["tasks"].insert_one(task_dict)

    # המרת `_id` ל- `id`
    task_dict["id"] = str(task_dict.pop("_id"))
    return TaskInDB(**task_dict)

@router.get("/{task_id}", response_model=TaskInDB)
async def get_task(task_id: str):
    """Retrieves a task by ID."""
    db = Database.get_database()

    if not ObjectId.is_valid(task_id):  
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    task = await db["tasks"].find_one({"_id": ObjectId(task_id)})
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task["id"] = str(task["_id"])
    task.pop("_id")
    return TaskInDB(**task)

@router.put("/{task_id}", response_model=TaskInDB)
async def update_task(task_id: str, task_update: TaskUpdate):
    """Updates an existing task."""
    db = Database.get_database()

    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    update_data = {k: v for k, v in task_update.model_dump().items() if v is not None}
    
    updated_task = await db["tasks"].find_one_and_update(
        {"_id": ObjectId(task_id)}, 
        {"$set": update_data}, 
        return_document=ReturnDocument.AFTER
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task["id"] = str(updated_task.pop("_id"))
    return TaskInDB(**updated_task)

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Deletes a task."""
    db = Database.get_database()

    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    result = await db["tasks"].delete_one({"_id": ObjectId(task_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}

@router.get("/", response_model=list[TaskInDB])
async def get_all_tasks():
    """Retrieves all tasks."""
    db = Database.get_database()
    tasks_cursor = db["tasks"].find()
    tasks = await tasks_cursor.to_list(length=None)

    for task in tasks:
        task["id"] = str(task["_id"])
        task.pop("_id") 

    return tasks