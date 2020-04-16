from typing import List
from uuid import uuid4

from fastapi import FastAPI

from task_manager.models import InputTask, Task

TASKS = []

app = FastAPI()


@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return TASKS


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: InputTask):
    new_task = task.dict()
    new_task.update({"id": uuid4()})
    TASKS.append(new_task)
    return new_task
