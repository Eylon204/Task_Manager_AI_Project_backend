import asyncio
from app.core.database import Database

async def test_connection():
    await Database.connect()
    db = Database.get_database()
    collections = await db.list_collection_names()
    print("✅ Collections in the database:", collections)

asyncio.run(test_connection())