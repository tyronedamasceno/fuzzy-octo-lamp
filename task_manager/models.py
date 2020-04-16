from pydantic import BaseModel, constr


class Task(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(max_length=140)
