from fastapi import FastAPI

from task_manager.tasks import router as tasks_router
from task_manager.security import router as security_router

app = FastAPI()
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(security_router, prefix="/auth", tags=["authentication"])
