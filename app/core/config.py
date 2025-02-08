import os
from dotenv import load_dotenv

load_dotenv()  # טוען משתני סביבה מקובץ .env

class Settings:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://eylon204:eylon2041@cluster1.wx9lw.mongodb.net/?retryWrites=true&w=majority")
    MONGO_DB_NAME = os.getenv("MON׳O_DB_NAME", "TaskManagerDB")

settings = Settings()