from uuid import UUID

from pydantic import BaseModel, constr

from task_manager.enums import PossibleStatus

TASKS = []


class InputTask(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(max_length=140)
    status: PossibleStatus = PossibleStatus.not_done


class Task(InputTask):
    id: UUID
