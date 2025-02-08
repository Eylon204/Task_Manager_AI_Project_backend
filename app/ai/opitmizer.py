from typing import List
from app.models.task import TaskInDB
from datetime import datetime, timedelta
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.linear_model import LinearRegression

# -------------------------------------------
# Deep Learning Model for Task Duration Prediction
# -------------------------------------------
class TaskDurationNN(nn.Module):
    """
    Deep Learning model for predicting task duration based on priority and user patterns.
    """
    def __init__(self):
        super(TaskDurationNN, self).__init__()
        self.fc1 = nn.Linear(2, 32)  # Priority + Historical workload
        self.fc2 = nn.Linear(32, 32)
        self.fc3 = nn.Linear(32, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def train_task_duration_nn(tasks: List[TaskInDB]):
    """
    Train a deep learning model to predict task duration based on priority and workload patterns.
    """
    if not tasks:
        return None
    
    durations = [task.estimated_time for task in tasks if task.estimated_time]
    priorities = [1 if task.priority == "high" else (0.5 if task.priority == "medium" else 0) for task in tasks]
    workloads = [task.user_workload if hasattr(task, 'user_workload') else 0.5 for task in tasks]  # Default workload factor
    
    if len(durations) < 5:
        return None  # Not enough data to train
    
    X = torch.tensor(list(zip(priorities, workloads)), dtype=torch.float32)
    y = torch.tensor(durations, dtype=torch.float32).view(-1, 1)
    
    model = TaskDurationNN()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    for epoch in range(1000):
        optimizer.zero_grad()
        predictions = model(X)
        loss = criterion(predictions, y)
        loss.backward()
        optimizer.step()
    
    return model

# -------------------------------------------
# Task Scheduling Algorithm with AI Learning
# -------------------------------------------
def optimize_task_schedule(tasks: List[TaskInDB]) -> List[TaskInDB]:
    """
    AI-based task optimizer that schedules tasks efficiently based on priority, workload, and deep learning predictions.
    """
    if not tasks:
        return []
    
    model_nn = train_task_duration_nn(tasks)
    
    # Sort tasks by priority and earliest due date
    sorted_tasks = sorted(tasks, key=lambda x: (x.priority, x.due_date or datetime.max), reverse=True)
    
    current_time = datetime.utcnow()
    work_hours_start = current_time.replace(hour=9, minute=0, second=0, microsecond=0)
    work_hours_end = current_time.replace(hour=18, minute=0, second=0, microsecond=0)
    buffer_time = timedelta(minutes=5)
    
    for task in sorted_tasks:
        # Predict duration using deep learning model
        if model_nn:
            with torch.no_grad():
                input_data = torch.tensor([[1 if task.priority == "high" else (0.5 if task.priority == "medium" else 0), 
                                            task.user_workload if hasattr(task, 'user_workload') else 0.5]], dtype=torch.float32)
                predicted_duration = model_nn(input_data).item()
        else:
            predicted_duration = task.estimated_time if task.estimated_time else 30
        
        task_duration = timedelta(minutes=max(15, min(predicted_duration, 120)))
        
        # Ensure scheduling within work hours
        if current_time < work_hours_start:
            current_time = work_hours_start
        elif current_time + task_duration > work_hours_end:
            current_time = work_hours_start + timedelta(days=1)
        
        task.scheduled_time = current_time
        task.due_date = current_time + task_duration
        current_time = task.due_date + buffer_time  # Move to next available slot
    
    return sorted_tasks
