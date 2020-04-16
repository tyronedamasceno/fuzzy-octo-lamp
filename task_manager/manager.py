from fastapi import FastAPI

TASKS = []

app = FastAPI()


@app.get("/tasks")
def list_tasks():
    return TASKS
