from fastapi.testclient import TestClient
from app.main import app
import pytest

from app.core.config import settings


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


def test_login_username(client: TestClient):
    login_data = {
        "username": settings.FIRST_SUPERUSER_USERNAME,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 201
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_login_email(client: TestClient):
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 201
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_login_wrong_username(client: TestClient):
    login_data = {"username": "wrong_username", "password": "wrong_password"}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 404


def test_login_wrong_password(client: TestClient):
    login_data = {
        "username": settings.FIRST_SUPERUSER_USERNAME,
        "password": "wrong_password",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400
