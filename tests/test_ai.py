import torch
from app.ai.opitmizer import TaskDurationNN, train_task_duration_nn
from app.models.task import TaskInDB


def test_train_task_duration_nn():
    """Tests training of the neural network model for task duration prediction."""
    tasks = [
        TaskInDB(title="Urgent Task", priority="high", estimated_time=60, user_id="test_user"),
        TaskInDB(title="Regular Task", priority="medium", estimated_time=45, user_id="test_user"),
        TaskInDB(title="Low Priority Task", priority="low", estimated_time=30, user_id="test_user"),
    ]
    model = train_task_duration_nn(tasks)
    assert model is not None
    assert isinstance(model, TaskDurationNN)


def test_neural_network_forward_pass():
    """Tests if the neural network can process inputs without errors."""
    model = TaskDurationNN()
    sample_input = torch.tensor([[1.0, 0.5]], dtype=torch.float32)
    output = model(sample_input)
    assert output.shape == (1, 1)