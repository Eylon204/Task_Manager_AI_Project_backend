from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument
from app.models.event import EventInDB, EventCreate, EventUpdate
from app.core.database import Database
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=EventInDB, status_code=201)
async def create_event(event: EventCreate):
    """Creates a new event."""
    event_dict = event.model_dump()
    event_dict["_id"] = ObjectId()
    db = Database.get_database()
    await db["events"].insert_one(event_dict)

    event_dict["id"] = str(event_dict.pop("_id"))  # Change _id to id
    return EventInDB(**event_dict)

@router.get("/{event_id}", response_model=EventInDB)
async def get_event(event_id: str):
    """Retrieves an event by ID."""
    db = Database.get_database()

    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID format")

    event = await db["events"].find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event["id"] = str(event["_id"])
    event.pop("_id")
    return EventInDB(**event)

@router.get("/", response_model=list[EventInDB])
async def get_all_events():
    """Retrieves all events."""
    db = Database.get_database()
    events_cursor = db["events"].find()
    events = await events_cursor.to_list(length=None)

    for event in events:
        event["id"] = str(event["_id"])
        event.pop("_id")  # Remove _id to prevent validation error

    return events

@router.put("/{event_id}", response_model=EventInDB)
async def update_event(event_id: str, event_update: EventUpdate):
    """Updates an existing event."""
    db = Database.get_database()

    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID format")

    update_data = {k: v for k, v in event_update.model_dump().items() if v is not None}
    updated_event = await db["events"].find_one_and_update(
        {"_id": ObjectId(event_id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )

    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")

    updated_event["id"] = str(updated_event.pop("_id"))
    return EventInDB(**updated_event)

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    """Deletes an event."""
    db = Database.get_database()

    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID format")

    result = await db["events"].delete_one({"_id": ObjectId(event_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"message": "Event deleted successfully"}