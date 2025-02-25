import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Task Manager AI"
    VERSION: str = "1.0"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your_secret_key")
    JWT_ALGORITHM: str = "HS256"
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/task_manager")

settings = Settings()