from fastapi import FastAPI

from task_manager.tasks import router

app = FastAPI()
app.include_router(router, prefix="/tasks")
