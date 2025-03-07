from motor.motor_asyncio import AsyncIOMotorClient
import os
import certifi 
from dotenv import load_dotenv

# 🚀 טוען משתני סביבה מ- `.env`
load_dotenv()

class Database:
    _client = None
    _db = None

    @classmethod
    async def connect(cls):
        """📡 התחברות ל-MongoDB עם תמיכה ב-SSL."""
        if cls._client is None:
            mongo_uri = os.getenv("MONGO_URI")
            if not mongo_uri:
                raise RuntimeError("❌ MONGO_URI is not set in .env file!")

            cls._client = AsyncIOMotorClient(mongo_uri, tlsCAFile=certifi.where())  # ✅ אבטחה מלאה
            cls._db = cls._client["task_manager"]
            print("✅ Successfully connected to MongoDB")

    @classmethod
    async def disconnect(cls):
        """🔌 ניתוק ממסד הנתונים"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            print("🔌 MongoDB connection closed")

    @classmethod
    def get_database(cls):
        """🔍 מחזיר את חיבור מסד הנתונים אם קיים"""
        if cls._db is None:
            raise RuntimeError("❌ Database is not connected! Call `await Database.connect()` first.")
        return cls._db