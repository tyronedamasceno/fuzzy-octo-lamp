from fastapi import FastAPI

from task_manager.models import Task

TASKS = []

app = FastAPI()


@app.get("/tasks")
def list_tasks():
    return TASKS


@app.post("/tasks")
def create_task(task: Task):
    return task
