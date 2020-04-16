from uuid import uuid4

from fastapi import FastAPI

from task_manager.models import InputTask, Task

TASKS = []

app = FastAPI()


@app.get("/tasks")
def list_tasks():
    return TASKS


@app.post("/tasks", response_model=Task)
def create_task(task: InputTask):
    new_task = task.dict()
    new_task.update({"id": uuid4()})
    return new_task
