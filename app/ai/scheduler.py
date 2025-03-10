import logging
from typing import List
import torch
from app.models.task_model import TaskInDB
from app.ai.train import prepare_training_data, train_task_duration_model

# הגדרת מערכת לוגים
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MODEL_PATH = "app/ai/task_duration_model.pth"

def load_or_train_model(tasks: List[TaskInDB]):
    """
    טוען את המודל המאומן אם קיים, אחרת מאמן ושומר מודל חדש.
    """
    try:
        model = torch.load(MODEL_PATH)
        model.eval()
        logger.info("✅ Loaded existing AI model from %s", MODEL_PATH)
        return model
    except FileNotFoundError:
        logger.warning("⚠️ No trained model found. Training a new one...")
        X, y = prepare_training_data(tasks)
        model = train_task_duration_model(X, y)
        torch.save(model, MODEL_PATH)
        logger.info("✅ New AI model trained and saved to %s", MODEL_PATH)
        return model

def predict_task_duration(model, task: TaskInDB) -> float:
    """
    מנבא את זמן המשימה בהתבסס על המודל המאומן.
    """
    priority = 1 if task.priority == "high" else (0.5 if task.priority == "medium" else 0)
    workload = task.user_workload if hasattr(task, 'user_workload') else 0.5
    X = torch.tensor([[priority, workload]], dtype=torch.float32)
    
    with torch.no_grad():
        predicted_duration = model(X).item()
    
    logger.info("🔍 Predicted duration for task '%s': %.2f minutes", task.title, predicted_duration)
    
    return max(predicted_duration, 15)  # מבטיח מינימום 15 דקות למשימה

def schedule_tasks(tasks: List[TaskInDB]) -> List[TaskInDB]:
    """
    תכנון חכם של סדר המשימות לפי חיזוי זמן ביצוע, עדיפות ותאריך יעד.
    """
    logger.info("📌 Starting AI-based task scheduling...")
    model = load_or_train_model(tasks)
    
    if model is None:
        logger.warning("⚠️ No AI model available. Falling back to simple sorting.")
        return sorted(tasks, key=lambda x: (x.priority, x.due_date or ""), reverse=True)
    
    for task in tasks:
        task.predicted_duration = predict_task_duration(model, task)
    
    sorted_tasks = sorted(tasks, key=lambda x: (-x.priority, x.due_date or "", x.predicted_duration))
    logger.info("✅ Task scheduling completed! Returning optimized task list.")
    return sorted_tasks