from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.database import Database
from app.core.security import verify_password, hash_password, create_access_token
from app.models.user import UserCreate
from bson import ObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", status_code=201)
async def register_user(user: UserCreate):
    """Register a new user with hashed password."""
    try:
        db = Database.get_database()

        existing_user = await db["users"].find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_dict = user.dict()
        user_dict["_id"] = str(ObjectId())
        user_dict["hashed_password"] = hash_password(user_dict.pop("password"))

        await db["users"].insert_one(user_dict)
        return {"message": "User registered successfully"}

    except Exception as e:
        print(f"❌ ERROR in register_user: {e}")  
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token."""
    db = Database.get_database()

    user = await db["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}