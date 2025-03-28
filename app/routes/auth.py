from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.database import Database
from app.core.security import verify_password, hash_password, create_access_token
from app.models.user_model import UserCreate
from bson import ObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/register", status_code=201)
async def register_user(user: UserCreate):
    print("📡 Received request at /api/auth/register")  # בדיקה אם הבקשה מגיעה
    db = Database.get_database()
    
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_dict["_id"] = str(ObjectId())
    user_dict["hashed_password"] = hash_password(user_dict.pop("password"))

    await db["users"].insert_one(user_dict)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token."""
    db = Database.get_database()

    print(f"📡 Login attempt for: {form_data.username}")

    user = await db["users"].find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    is_password_valid = verify_password(form_data.password, user["hashed_password"])
    if not is_password_valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"]})

    # ✅ הוספת ה-ID למענה
    return {
        "access_token": token, 
        "token_type": "bearer", 
        "id": str(user["_id"]),  
        "email": user["email"], 
        "username": user.get("username", "Unknown")
    }