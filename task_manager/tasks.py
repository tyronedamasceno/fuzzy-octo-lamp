from typing import List
from uuid import uuid4, UUID

from fastapi import APIRouter, HTTPException

from task_manager.enums import SortingKeys
from task_manager.schemas import InputTask, Task, TASKS

router = APIRouter()


@router.get("", response_model=List[Task])
async def list_tasks(sort: bool = False,
                     sort_by: SortingKeys = SortingKeys.title):
    if sort:
        return sorted(TASKS, key=lambda t: t.get(sort_by))
    return TASKS


@router.get("/{task_id}", response_model=Task)
async def retrieve_task(task_id: UUID):
    task = list(filter(lambda task: task["id"] == task_id, TASKS))
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    return task[0]


@router.post("", response_model=Task, status_code=201)
async def create_task(task: InputTask):
    new_task = task.dict()
    new_task.update({"id": uuid4()})
    TASKS.append(new_task)
    return new_task


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID):
    tasks_to_remove = list(filter(lambda task: task["id"] == task_id, TASKS))
    if not tasks_to_remove:
        raise HTTPException(status_code=404, detail="Not found")
    TASKS.remove(tasks_to_remove[0])
    return
