from fastapi import FastAPI
<<<<<<< HEAD
from app.routes import user, task, calendar, ai, event
=======
from app.routes import user, task, calendar, ai, event, auth
>>>>>>> 07eae6ae (Added new backend files and updated repository)
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
<<<<<<< HEAD
=======
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
>>>>>>> 07eae6ae (Added new backend files and updated repository)
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(task.router, prefix="/tasks", tags=["tasks"])
app.include_router(event.router, prefix="/events", tags=["events"]) 
app.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
app.include_router(ai.router, prefix="/ai", tags=["AI"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Manager AI"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)