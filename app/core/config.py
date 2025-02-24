import os
from dotenv import load_dotenv

load_dotenv()  # טוען משתני סביבה מקובץ .env

class Settings:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://eylon204:eylon2041@cluster1.wx9lw.mongodb.net/?retryWrites=true&w=majority")
<<<<<<< HEAD
    MONGO_DB_NAME = os.getenv("MON׳O_DB_NAME", "TaskManagerDB")
=======
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "TaskManagerDB")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
>>>>>>> 07eae6ae (Added new backend files and updated repository)

settings = Settings()