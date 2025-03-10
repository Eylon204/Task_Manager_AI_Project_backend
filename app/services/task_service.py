from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from app.models.task_model import TaskInDB

# Initialize MongoDB connection
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["task_manager"]
task_collection = db["tasks"]

def get_all_tasks(user_id: str) -> List[TaskInDB]:
    """
    Retrieves all tasks for a given user from the database.
    """
    tasks = task_collection.find({"user_id": user_id})
    return [TaskInDB(**task) for task in tasks]

def get_task_by_id(task_id: str) -> Optional[TaskInDB]:
    """Retrieves a specific task by its ID."""
    try:
        task = task_collection.find_one({"_id": ObjectId(task_id)})
    except Exception:
        return None

    if task:
        return TaskInDB(**task)

    return None

def create_task(task: TaskInDB) -> TaskInDB:
    """
    Creates a new task and saves it to the database.
    """
    task_dict = task.dict(exclude={"id"})
    task_dict["created_at"] = datetime.utcnow()
    task_dict["updated_at"] = datetime.utcnow()
    inserted_id = task_collection.insert_one(task_dict).inserted_id
    task.id = str(inserted_id)
    return task

def update_task(task_id: str, task_data: dict) -> Optional[TaskInDB]:
    """
    Updates an existing task with new data.
    """
    task_data["updated_at"] = datetime.utcnow()
    result = task_collection.find_one_and_update(
        {"_id": ObjectId(task_id)},
        {"$set": task_data},
        return_document=True
    )
    if result:
        return TaskInDB(**result)
    return None

def delete_task(task_id: str) -> bool:
    """
    Deletes a task from the database.
    """
    result = task_collection.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count > 0
