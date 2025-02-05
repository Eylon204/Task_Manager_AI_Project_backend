# backend/app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Task Manager AI"
    VERSION: str = "1.0"
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017/task_manager")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your_secret_key")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()