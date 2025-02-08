from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument
from app.models.user import UserInDB, UserCreate, UserUpdate
from app.core.database import Database
from bson import ObjectId

router = APIRouter() 
@router.post("/", response_model=UserInDB, status_code=201)
async def create_user(user: UserCreate):
    """Creates a new user."""
    user_dict = user.model_dump()
    user_dict["_id"] = str(ObjectId()) 
    db = Database.get_database()
    await db["users"].insert_one(user_dict)

    user_dict["id"] = user_dict.pop("_id")
    return UserInDB(**user_dict)

@router.get("/{user_id}", response_model=UserInDB)
async def get_user(user_id: str):
    """Retrieves a user by ID."""
    db = Database.get_database()
    if not ObjectId.is_valid(user_id): 
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    return UserInDB(**user)


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: str, user_update: UserUpdate):
    """Updates an existing user."""
    db = Database.get_database()
    
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
    
    updated_user = await db["users"].find_one_and_update(
        {"_id": ObjectId(user_id)}, 
        {"$set": update_data}, 
        return_document=ReturnDocument.AFTER
    )

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    # המרת `_id` ל- `id`
    updated_user["id"] = str(updated_user.pop("_id"))

    return UserInDB(**updated_user)


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Deletes a user."""
    db = Database.get_database()
    
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})  

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}

@router.get("/", response_model=list[UserInDB])
async def get_all_users():
    """Retrieves all users."""
    db = Database.get_database()
    users_cursor = db["users"].find()
    users = await users_cursor.to_list(length=None)
    for user in users:
        user["id"] = str(user["_id"]) 

    return users