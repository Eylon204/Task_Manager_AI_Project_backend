from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument
from app.models.event_model import EventInDB, EventCreate, EventUpdate
from app.core.database import Database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=EventInDB, status_code=201)
async def create_event(event: EventCreate):
    """יוצר אירוע חדש עם ID תקין"""
    db = Database.get_database()
    
    event_dict = event.dict()
    event_dict["_id"] = ObjectId()  # ✅ יצירת ObjectId אמיתי
    await db["events"].insert_one(event_dict)

    # ✅ ווידוא שה-ID מוחזר כהלכה ל-Frontend
    event_dict["id"] = str(event_dict["_id"])
    event_dict.pop("_id")

    return EventInDB(**event_dict)

@router.get("/{event_id}", response_model=EventInDB)
async def get_event(event_id: str):
    """Returns an event by its ID."""
    db = Database.get_database()

    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID format")

    event = await db["events"].find_one({"_id": ObjectId(event_id)})

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event["id"] = str(event["_id"])
    
    if "date" in event and isinstance(event["date"], datetime):
        event["date"] = event["date"].isoformat()

    return EventInDB(**event)

@router.put("/{event_id}", response_model=EventInDB)
async def update_event(event_id: str, event_update: EventUpdate):
    """Updates an existing event by ID (_id)"""
    db = Database.get_database()

    if not ObjectId.is_valid(event_id):
        print("❌ Invalid event ID format:", event_id)
        raise HTTPException(status_code=400, detail="Invalid event ID format")

    update_data = {k: v for k, v in event_update.model_dump().items() if v is not None}
    print(f"🔄 Updating event {event_id} with data:", update_data)

    updated_event = await db["events"].find_one_and_update(
        {"_id": ObjectId(event_id)}, 
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )

    if not updated_event:
        print(f"❌ Event with ID {event_id} not found")
        raise HTTPException(status_code=404, detail="Event not found")

    updated_event["id"] = str(updated_event["_id"])
    updated_event.pop("_id", None)

    print("✅ Updated event:", updated_event)
    return EventInDB(**updated_event)

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    """מוחק אירוע לפי ID"""
    db = Database.get_database()

    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID format")

    result = await db["events"].delete_one({"_id": ObjectId(event_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"message": "Event deleted successfully"}

@router.get("/", response_model=list[EventInDB])
async def get_all_events():
    db = Database.get_database()
    events_cursor = db["events"].find()
    events = await events_cursor.to_list(length=None)

    for event in events:
        event["id"] = str(event.pop("_id", ""))  # ✅ המרת ObjectId למחרוזת ושינוי שם ל-id

    return events