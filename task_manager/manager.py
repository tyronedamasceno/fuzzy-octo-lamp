from fastapi import FastAPI

app = FastAPI()


@app.get("/tasks")
def list_tasks():
    return []
