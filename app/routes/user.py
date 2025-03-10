from fastapi import APIRouter, HTTPException, Depends
from pymongo import ReturnDocument
from app.models.user_model import UserInDB, UserCreate, UserUpdate
from app.core.database import Database
from app.core.security import get_current_user
from bson import ObjectId
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=UserInDB, status_code=201)
async def create_user(user: UserCreate):
    """Creates a new user."""
    db = Database.get_database()

    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    user_dict = user.dict()
    user_dict["_id"] = str(ObjectId())  

    await db["users"].insert_one(user_dict)

    user_dict["id"] = user_dict.pop("_id")
    logger.info(f"✅ User created successfully: {user_dict['id']}")
    return UserInDB(**user_dict)

@router.get("/{user_id}", response_model=UserInDB)
async def get_user(user_id: str, current_user: str = Depends(get_current_user)):
    db = Database.get_database()
    if not ObjectId.is_valid(user_id): 
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ הוספת id במקום _id
    user["id"] = str(user["_id"])
    del user["_id"]  # מחיקה כדי למנוע כפילות

    return UserInDB(**user)

@router.get("/", response_model=list[UserInDB])
async def get_all_users(current_user: str = Depends(get_current_user)):
    """Retrieves all users (🔐 Requires authentication)."""
    db = Database.get_database()
    users_cursor = db["users"].find()
    users = await users_cursor.to_list(length=None)
    
    for user in users:
        user["id"] = str(user["_id"]) 

    return users

@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: str, user_update: UserUpdate, current_user: str = Depends(get_current_user)):
    """Updates an existing user (🔐 Requires authentication)."""
    db = Database.get_database()

    if current_user != user_id:
        logger.warning(f"🚫 Unauthorized update attempt on user: {user_id}")
        raise HTTPException(status_code=403, detail="You can only update your own account")
    
    if not ObjectId.is_valid(user_id):
        logger.error("❌ Invalid user ID format")
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    update_data = {k: v for k, v in user_update.dict().items() if v is not None}

    if "password" in update_data:
        # כאן ניתן להוסיף פונקציה להצפנת הסיסמה
        update_data["password"] = "hashed_password"

    updated_user = await db["users"].find_one_and_update(
        {"_id": ObjectId(user_id)}, 
        {"$set": update_data}, 
        return_document=ReturnDocument.AFTER
    )

    if not updated_user:
        logger.error(f"❌ User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    updated_user["id"] = str(updated_user.pop("_id"))
    logger.info(f"✅ User updated successfully: {user_id}")
    return UserInDB(**updated_user)

@router.delete("/{user_id}")
async def delete_user(user_id: str, current_user: str = Depends(get_current_user)):
    """Deletes a user (🔐 Requires authentication)."""
    db = Database.get_database()

    if current_user != user_id:
        logger.warning(f"🚫 Unauthorized delete attempt on user: {user_id}")
        raise HTTPException(status_code=403, detail="You can only delete your own account")

    if not ObjectId.is_valid(user_id):
        logger.error("❌ Invalid user ID format")
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})  

    if result.deleted_count == 0:
        logger.error(f"❌ User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"✅ User deleted successfully: {user_id}")
    return {"message": "User deleted successfully"}