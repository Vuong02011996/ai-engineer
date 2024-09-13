from fastapi.testclient import TestClient
from fastapi import FastAPI
from odmantic import Model
from pydantic import BaseModel
from app.db.session import get_engine


class ExampleModel(Model):
    name: str
    age: int


class ExampleCreateSchema(BaseModel):
    name: str
    age: int


app = FastAPI()


@app.post("/create", status_code=200)
def create_something(request: ExampleCreateSchema) -> ExampleModel:
    engine = get_engine()
    example = ExampleModel(**request.dict())
    return engine.save(example)


def test_connect_db(client: TestClient):
    request = ExampleCreateSchema(name="Thanh", age="25").model_dump()
    r = client.post("localhost:8000/create", json=request)
    assert r.status_code == 201
