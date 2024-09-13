import pytest
from fastapi.testclient import TestClient
from collections.abc import Generator
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers
from app.main import app
from app.db.session import MongoDatabase


@pytest.fixture(scope="session")
def db() -> Generator:
    db = MongoDatabase()
    yield db


@pytest.fixture(scope="session")
def client(db) -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient) -> dict[str, str]:
    return authentication_token_from_email(client=client, email="u@u.u", db=db)


@pytest.fixture(scope="module")
def normal_user2_token_headers(client: TestClient) -> dict[str, str]:
    return authentication_token_from_email(client=client, email="u2@u.u", db=db)
