from sqlalchemy.orm import Session

from task_manager import db_models, schemas


def list_tasks(db: Session):
    return db.query(db_models.Task).all()


def create_task(db: Session, task: schemas.TaskCreate):
    new_task = db_models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
