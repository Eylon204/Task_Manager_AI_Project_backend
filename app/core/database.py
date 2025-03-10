from motor.motor_asyncio import AsyncIOMotorClient
import os
import certifi 
from dotenv import load_dotenv
import logging

# 🚀 טעינת משתני סביבה מ- `.env`
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")

class Database:
    _client = None
    _db = None

    @classmethod
    async def connect(cls):
        """📡 התחברות ל-MongoDB עם תמיכה ב-SSL, כולל בדיקות חיבור"""
        if cls._client is None:
            mongo_uri = os.getenv("MONGO_URI")
            if not mongo_uri:
                logger.error("❌ MONGO_URI is not set in .env file!")
                raise RuntimeError("MONGO_URI is missing!")
            
            try:
                cls._client = AsyncIOMotorClient(mongo_uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
                cls._db = cls._client["task_manager"]
                # בדיקה שהחיבור פעיל
                await cls._client.server_info()
                logger.info("✅ Successfully connected to MongoDB")
            except Exception as e:
                logger.error(f"❌ Failed to connect to MongoDB: {e}")
                raise RuntimeError("Database connection failed!")

    @classmethod
    async def disconnect(cls):
        """🔌 ניתוק ממסד הנתונים"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("🔌 MongoDB connection closed")

    @classmethod
    def get_database(cls):
        """🔍 מחזיר את חיבור מסד הנתונים אם קיים"""
        if cls._db is None:
            logger.error("❌ Database is not connected! Call `await Database.connect()` first.")
            raise RuntimeError("Database is not connected!")
        return cls._db
