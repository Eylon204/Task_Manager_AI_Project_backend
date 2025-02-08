from typing import List
from app.models.task import TaskInDB

def schedule_tasks(tasks: List[TaskInDB]) -> List[TaskInDB]:
    """
    AI-based scheduling algorithm to optimize task order based on priority and due date.
    """

# Sort tasks by priority (high > medium > low) and then by due date
    sorted_tasks = sorted(tasks, key=lambda x: (x.priority, x.due_date or ""), reverse=True)
    return sorted_tasks