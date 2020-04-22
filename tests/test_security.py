from starlette import status
from starlette.testclient import TestClient

from task_manager.manager import app


def test_trying_authenticate_with_invalid_credentials_returns_401():
    client = TestClient(app)
    resp = client.post("/auth/token", data={
        "username": "tyrone", "password": "banana"})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticate_with_correct_credentials_return_200():
    client = TestClient(app)
    resp = client.post("/auth/token", data={
        "username": "tyrone", "password": "secret"})
    assert resp.status_code == status.HTTP_200_OK


def test_calling_me_endpoint_without_authentication_return_401():
    client = TestClient(app)
    resp = client.get("/auth/users/me")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_calling_me_endpoint_with_authentication_return_200():
    client = TestClient(app)
    get_token_resp = client.post("/auth/token", data={
        "username": "tyrone", "password": "secret"})
    token = get_token_resp.json()['access_token']
    resp = client.get("/auth/users/me",
                      headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK
