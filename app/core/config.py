import os
from dotenv import load_dotenv

# 🚀 טעינת משתני סביבה מ- `.env`
load_dotenv()

class Settings:
    """📌 קביעת משתני מערכת (Configuration Settings)"""

    # 🏷️ הגדרות מערכת
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Task Manager AI")
    VERSION: str = os.getenv("VERSION", "1.0")

    # 🔐 הגדרות JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your_secret_key")  # מפתח סודי ל-JWT
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")  # אלגוריתם הצפנה
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # תוקף טוקן בדקות

    # 🛢️ הגדרות מסד נתונים
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/task_manager")  # URI של MongoDB

    # 🛠️ מצב דיבאג (Debug Mode)
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() in ["true", "1"]  # הפעלת מצב Debug

# יצירת מופע של ההגדרות
settings = Settings()

print("🏷️ Project:", settings.PROJECT_NAME)
print("🔐 JWT_SECRET_KEY:", settings.JWT_SECRET_KEY)
print("📡 MONGO_URI:", settings.MONGO_URI)
print("🕒 Token Expiry:", settings.ACCESS_TOKEN_EXPIRE_MINUTES, "minutes")
print("🐞 Debug Mode:", settings.DEBUG_MODE)