from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK

from task_manager.manager import app, TASKS


def test_listing_tasks_should_return_200():
    client = TestClient(app)
    resp = client.get("/tasks")
    assert resp.status_code == HTTP_200_OK


def test_listing_tasks_should_return_json():
    client = TestClient(app)
    resp = client.get("/tasks")
    assert resp.headers["Content-Type"] == "application/json"


def test_listing_tasks_should_return_list():
    client = TestClient(app)
    resp = client.get("/tasks")
    assert isinstance(resp.json(), list)


def test_listing_tasks_return_one_task_with_id():
    TASKS.append({"id": 1})
    client = TestClient(app)
    resp = client.get("/tasks")
    assert "id" in resp.json().pop()
    TASKS.clear()


def test_listing_tasks_return_one_task_with_title():
    TASKS.append({"title": "test task"})
    client = TestClient(app)
    resp = client.get("/tasks")
    assert "title" in resp.json().pop()
    TASKS.clear()


def test_listing_tasks_return_one_task_with_description():
    TASKS.append({"description": "this is a really nice task"})
    client = TestClient(app)
    resp = client.get("/tasks")
    assert "description" in resp.json().pop()
    TASKS.clear()


def test_listing_tasks_return_one_task_with_status():
    TASKS.append({"status": "done"})
    client = TestClient(app)
    resp = client.get("/tasks")
    assert "status" in resp.json().pop()
    TASKS.clear()
