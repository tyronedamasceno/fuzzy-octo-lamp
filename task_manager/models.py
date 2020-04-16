from enum import Enum
from uuid import UUID

from pydantic import BaseModel, constr


class PossibleStatus(str, Enum):
    not_done = "not done"
    in_progress = "in progress"
    done = "done"


class InputTask(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(max_length=140)
    status: PossibleStatus = PossibleStatus.not_done


class Task(InputTask):
    id: UUID
