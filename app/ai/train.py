import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from app.models.task import TaskInDB
from app.ai.opitmizer import TaskDurationNN
from typing import List

def prepare_training_data(tasks: List[TaskInDB]):
    """
    Prepares data for training the model based on priority, workload, and estimated time.
    """
    priorities = [1 if task.priority == "high" else (0.5 if task.priority == "medium" else 0) for task in tasks]
    workloads = [task.user_workload if hasattr(task, 'user_workload') else 0.5 for task in tasks]
    durations = [task.estimated_time for task in tasks if task.estimated_time]

    if len(durations) < 5:
        raise ValueError("Not enough data to train the model.")

    X = torch.tensor(list(zip(priorities, workloads)), dtype=torch.float32)
    y = torch.tensor(durations, dtype=torch.float32).view(-1, 1)

    return X, y

def train_task_duration_model(tasks: List[TaskInDB], epochs: int = 1000, lr: float = 0.01):
    """
    Trains the Deep Learning model for predicting task completion times.
    """
    if not tasks:
        raise ValueError("No tasks available for training.")

    X, y = prepare_training_data(tasks)

    model = TaskDurationNN()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        optimizer.zero_grad()
        predictions = model(X)
        loss = criterion(predictions, y)
        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print(f"Epoch {epoch}/{epochs}, Loss: {loss.item()}")

    return model

if __name__ == "__main__":
    # Replace this with real tasks from the database
    sample_tasks = [
        TaskInDB(title="Urgent Task", priority="high", estimated_time=60, user_id="test_user"),
        TaskInDB(title="Regular Task", priority="medium", estimated_time=45, user_id="test_user"),
        TaskInDB(title="Low Priority Task", priority="low", estimated_time=30, user_id="test_user"),
    ]
    
    trained_model = train_task_duration_model(sample_tasks)
    torch.save(trained_model.state_dict(), "backend/app/models/task_duration_model.pth")
    print("Model trained and saved successfully.")
