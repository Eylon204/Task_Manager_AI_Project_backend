# backend/app/core/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

    @staticmethod
    async def connect():
        Database.client = AsyncIOMotorClient(settings.MONGODB_URL)
        Database.db = Database.client.get_database("task_manager")
        print("✅ Connected to MongoDB")

    @staticmethod
    async def disconnect():
        if Database.client:
            Database.client.close()
            print("❌ Disconnected from MongoDB")