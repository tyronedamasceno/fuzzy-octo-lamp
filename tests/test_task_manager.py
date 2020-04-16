from copy import copy
from uuid import uuid4

from starlette import status
from starlette.testclient import TestClient

from task_manager.manager import app, TASKS
from task_manager.models import PossibleStatus, Task

DEFAULT_TASK = Task(id=uuid4(), title="nice title",
                    description="this is a really nice task")


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
    TASKS.append(copy(DEFAULT_TASK.dict()))
    client = TestClient(app)
    resp = client.get("/tasks")
    assert "id" in resp.json().pop()
    TASKS.clear()


def test_listing_tasks_return_one_task_with_title():
    TASKS.append(copy(DEFAULT_TASK.dict()))
    client = TestClient(app)
    resp = client.get("/tasks")
    assert "title" in resp.json().pop()
    TASKS.clear()


def test_listing_tasks_return_one_task_with_description():
    TASKS.append(copy(DEFAULT_TASK.dict()))
    client = TestClient(app)
    resp = client.get("/tasks")
    assert "description" in resp.json().pop()
    TASKS.clear()


def test_listing_tasks_return_one_task_with_status():
    TASKS.append(copy(DEFAULT_TASK.dict()))
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
    resp_json = resp.json()
    resp_json.pop("id")
    resp_json.pop("status")
    assert resp_json == task_payload
    TASKS.clear()


def test_creating_task_should_return_an_unique_id():
    client = TestClient(app)
    task_payload1 = {"title": "nice title", "description": "hey apple"}
    task_payload2 = {"title": "title monster", "description": "something"}
    resp1 = client.post("/tasks", json=task_payload1)
    resp2 = client.post("/tasks", json=task_payload2)
    assert resp1.json()["id"] != resp2.json()["id"]
    TASKS.clear()


def test_created_task_has_default_status_not_done():
    client = TestClient(app)
    task_payload = {"title": "nice title", "description": "hey apple"}
    resp = client.post("/tasks", json=task_payload)
    assert resp.json()["status"] == PossibleStatus.not_done
    TASKS.clear()


def test_creating_task_should_return_201():
    client = TestClient(app)
    task_payload = {"title": "nice title", "description": "hey apple"}
    resp = client.post("/tasks", json=task_payload)
    assert resp.status_code == status.HTTP_201_CREATED
    TASKS.clear()


def test_creating_task_should_add_to_tasks_list():
    client = TestClient(app)
    task_payload = {"title": "nice title", "description": "hey apple"}
    client.post("/tasks", json=task_payload)
    assert len(TASKS) == 1
    TASKS.clear()


def test_retrieving_task_with_invalid_id_return_404():
    client = TestClient(app)
    resp = client.get(f"/tasks/{uuid4()}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_retrieving_task_ok_return_200():
    TASKS.append(copy(DEFAULT_TASK.dict()))
    client = TestClient(app)
    resp = client.get(f"/tasks/{DEFAULT_TASK.id}")
    assert resp.status_code == status.HTTP_200_OK
    TASKS.clear()
