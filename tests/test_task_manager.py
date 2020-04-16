from starlette import status
from starlette.testclient import TestClient

from task_manager.manager import app, TASKS


def test_listing_tasks_should_return_200():
    client = TestClient(app)
    resp = client.get("/tasks")
    assert resp.status_code == status.HTTP_200_OK


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


def test_task_resource_should_accept_post():
    client = TestClient(app)
    resp = client.post("/tasks")
    assert resp.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


def test_created_task_should_have_title():
    client = TestClient(app)
    resp = client.post("/tasks", json={})
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_created_task_title_should_have_at_least_3_characters():
    client = TestClient(app)
    resp = client.post("/tasks", json={"title": "aa"})
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_created_task_title_should_have_at_most_50_characters():
    client = TestClient(app)
    resp = client.post("/tasks", json={"title": 51 * "a"})
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_created_task_description_should_have_at_most_140_characters():
    client = TestClient(app)
    task_payload = {"title": "nice title", "description": 141 * "a"}
    resp = client.post("/tasks", json=task_payload)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_task_endpoint_should_return_created_task_itself():
    client = TestClient(app)
    task_payload = {"title": "nice title", "description": "hey apple"}
    resp = client.post("/tasks", json=task_payload)
    assert resp.json() == task_payload
