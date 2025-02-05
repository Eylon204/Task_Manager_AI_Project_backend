# backend/app/main.py
from fastapi import FastAPI
# from app.routes import user, task, calendar, ai
from app.core.database import Database
from app.core.config import Settings

app = FastAPI(title="Task Manager AI", version="1.0")

@app.on_event("startup")
async def startup_db():
    await Database.connect()

@app.on_event("shutdown")
async def shutdown_db():
    await Database.disconnect()

# Include routes
# app.include_router(user.router, prefix="/users", tags=["Users"])
# app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
# app.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
# app.include_router(ai.router, prefix="/ai", tags=["AI"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Manager AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)