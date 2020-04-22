from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr

from task_manager.enums import PossibleStatus

TASKS = []

fake_users_db = {
    "tyrone": {
        "username": "tyrone",
        "email": "tyronedamasceno@gmail.com",
        "hashed_password":
            "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_active": True,
    }
}


class InputTask(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(max_length=140)
    status: PossibleStatus = PossibleStatus.not_done


class Task(InputTask):
    id: UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: Optional[str]
    is_active: bool = True


class UserInDB(User):
    hashed_password: str
