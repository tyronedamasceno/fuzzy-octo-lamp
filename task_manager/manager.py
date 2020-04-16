from typing import List
from uuid import uuid4, UUID

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from task_manager.enums import SortingKeys
from task_manager.models import InputTask, Task

TASKS = []

app = FastAPI()


@app.get("/tasks", response_model=List[Task])
async def list_tasks(sort: bool = False, sort_by: SortingKeys = SortingKeys.title):
    if sort:
        return sorted(TASKS, key=lambda t: t.get(sort_by))
    return TASKS


@app.get("/tasks/{task_id}", response_model=Task)
async def retrieve_task(task_id: UUID):
    task = list(filter(lambda task: task["id"] == task_id, TASKS))
    if not task:
        return JSONResponse(status_code=404)
    return task[0]


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: InputTask):
    new_task = task.dict()
    new_task.update({"id": uuid4()})
    TASKS.append(new_task)
    return new_task
