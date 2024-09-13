import pytest
from fastapi.testclient import TestClient
from collections.abc import Generator
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
