from motor.motor_asyncio import AsyncIOMotorClient
import os
import certifi  # ✅ מוסיף תמיכה בתעודות SSL תקינות
from dotenv import load_dotenv

load_dotenv()

class Database:
    _client = None
    _db = None

    @classmethod
    async def connect(cls):
        """Connect to MongoDB using SSL certificate verification."""
        if cls._client is None:
            cls._client = AsyncIOMotorClient(
                os.getenv("MONGO_URI"), tlsCAFile=certifi.where()  # ✅ תמיכה מלאה ב-SSL
            )
            cls._db = cls._client["task_manager"]
            print("✅ Connected to MongoDB")

    @classmethod
    async def disconnect(cls):
        """Disconnect from MongoDB"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            print("✅ Disconnected from MongoDB")

    @classmethod
    def get_database(cls):
        """Returns the database instance"""
        if cls._db is None:
            raise RuntimeError("❌ Database is not connected! Call `await Database.connect()` first.")
        return cls._db