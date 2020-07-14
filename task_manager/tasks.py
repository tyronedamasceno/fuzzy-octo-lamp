from typing import List
from uuid import uuid4, UUID

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from task_manager import crud, db_models
from task_manager.database import SessionLocal, engine
from task_manager.enums import SortingKeys
from task_manager.schemas import TaskBase, Task, TASKS

router = APIRouter()

db_models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=List[Task])
async def list_tasks(sort: bool = False,
                     sort_by: SortingKeys = SortingKeys.title,
                     db: Session = Depends(get_db)):
    # if sort:
    #     return sorted(TASKS, key=lambda t: t.get(sort_by))
    return crud.list_tasks(db)


@router.get("/{task_id}", response_model=Task)
async def retrieve_task(task_id: UUID):
    task = list(filter(lambda task: task["id"] == task_id, TASKS))
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    return task[0]


@router.post("", response_model=Task, status_code=201)
async def create_task(task: TaskBase, db: Session = Depends(get_db)):
    new_task = crud.create_task(db, task)
    return new_task


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID):
    tasks_to_remove = list(filter(lambda task: task["id"] == task_id, TASKS))
    if not tasks_to_remove:
        raise HTTPException(status_code=404, detail="Not found")
    TASKS.remove(tasks_to_remove[0])
    return
