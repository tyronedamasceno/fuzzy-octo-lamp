from uuid import UUID

from pydantic import BaseModel, constr


class InputTask(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(max_length=140)


class Task(InputTask):
    id: UUID
