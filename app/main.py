from fastapi import FastAPI
from app.routes import user, task, calendar, ai, event, auth
from app.core.database import Database

app = FastAPI(title="Task Manager AI", version="1.0")

@app.on_event("startup")
async def startup_db():
    """Ensure database is initialized on startup."""
    await Database.connect() 

@app.on_event("shutdown")
async def shutdown_db():
    await Database.disconnect()  

# The Routes:
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(task.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(event.router, prefix="/api/events", tags=["events"]) 
app.include_router(calendar.router, prefix="/api/calendar", tags=["calendar"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])

from fastapi.middleware.cors import CORSMiddleware

# 🛠️ הגדרת CORS - מתיר לכל המקורות, אם רוצים להקשיח אפשר להגדיר דומיינים ספציפיים
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ניתן להחליף ברשימת מקורות ספציפיים למשל ["http://localhost:4200"]
    allow_credentials=True,
    allow_methods=["*"],  # מתיר את כל סוגי הבקשות (כולל POST)
    allow_headers=["*"],  # מתיר את כל הכותרות
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Manager AI"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)