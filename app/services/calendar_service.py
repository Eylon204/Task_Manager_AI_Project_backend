import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.models.task import TaskInDB
from typing import List
from datetime import datetime, timedelta

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_JSON", "/Users/eylonlevy/Desktop/Task Manger AI-Final Project/backend/app/core/google_service_account.json"
)

# בדיקה שהקובץ אכן קיים
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    raise FileNotFoundError(f"Google Service Account file not found: {SERVICE_ACCOUNT_FILE}")

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

def sync_with_google_calendar(tasks: List[TaskInDB]) -> List[TaskInDB]:
    """
    Syncs tasks with Google Calendar events.
    """
    service = build("calendar", "v3", credentials=credentials)
    calendar_id = "primary"

    for task in tasks:
        if not task.due_date:
            task.due_date = datetime.utcnow() + timedelta(days=1)  # ברירת מחדל: יום לאחר יצירת המשימה

        event = {
            "summary": task.title,
            "description": task.description or "No description",
            "start": {"dateTime": task.due_date.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": (task.due_date + timedelta(hours=1)).isoformat(), "timeZone": "UTC"},  # ברירת מחדל של שעה
        }
        
        try:
            service.events().insert(calendarId=calendar_id, body=event).execute()
        except Exception as e:
            print(f"❌ Error syncing task '{task.title}' with Google Calendar: {e}")

    return tasks