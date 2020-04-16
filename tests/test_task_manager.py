from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK

from task_manager.manager import app


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
