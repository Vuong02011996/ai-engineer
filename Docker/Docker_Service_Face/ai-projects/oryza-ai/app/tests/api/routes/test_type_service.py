from fastapi.testclient import TestClient
from faker import Faker

from app.core.config import settings
from app.schemas.type_service_schemas import TypeServiceCreate, TypeServiceUpdate
from app.services import type_service_services
from app.tests.init_db import init_data as data

fake = Faker()


def test_create_type_service(
    client: TestClient,
    superuser_token_headers: dict,
):
    type_service_data = TypeServiceCreate(
        name=fake.name(),  # Generate a random
        key=fake.name(),  # Generate a random
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/type_service/create",
        headers=superuser_token_headers,
        json=type_service_data,
    )
    assert r.status_code == 201
    created_type_service = r.json()
    assert created_type_service["name"] == type_service_data["name"]
    assert created_type_service["key"] == type_service_data["key"]
    # Remove the created type service
    try:
        type_service_services.remove(id=created_type_service["id"])
    except Exception as e:
        print(e)


def test_create_type_service_duplicate(
    client: TestClient,
    superuser_token_headers: dict,
):
    type_service2 = data["type_service"][1]
    type_service_data = TypeServiceCreate(
        name=type_service2["name"], key=type_service2["key"]
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/type_service/create",
        headers=superuser_token_headers,
        json=type_service_data,
    )
    assert r.status_code == 400
    assert (
        r.json()["detail"] == "Name already used"
        or r.json()["detail"] == "Key already used"
    )


def test_create_type_service_no_permission(
    client: TestClient,
    normal_user_token_headers: dict,
):
    fake = Faker()
    type_service_data = TypeServiceCreate(
        name=fake.name(),  # Generate a random
        key=fake.name(),  # Generate a random
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/type_service/create",
        headers=normal_user_token_headers,
        json=type_service_data,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Not enough permissions"


def test_get_type_services(
    client: TestClient,
    normal_user_token_headers: dict,
):
    r = client.get(
        f"{settings.API_V1_STR}/type_service/get_all",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    type_services = r.json()["data"]
    assert type_services
    for type_service in type_services:
        assert "name" in type_service
        assert "key" in type_service
    assert len(type_services) == len(data["type_service"])


def test_get_type_service_by_id(
    client: TestClient,
    normal_user_token_headers: dict,
):
    type_service2 = data["type_service"][1]
    r = client.get(
        f"{settings.API_V1_STR}/type_service/get_by_id/{type_service2['id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    type_service = r.json()
    assert type_service
    assert type_service["name"] == type_service2["name"]
    assert type_service["key"] == type_service2["key"]


def test_get_type_service_by_id_not_found(
    client: TestClient,
    normal_user_token_headers: dict,
):
    fake_id = "66372d0de0efbcb3d9b331b5"
    r = client.get(
        f"{settings.API_V1_STR}/type_service/get_by_id/{fake_id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Type service not found"


def test_count_type_services(
    client: TestClient,
    normal_user_token_headers: dict,
):
    r = client.get(
        f"{settings.API_V1_STR}/type_service/count",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    assert r.json()["count"] == len(data["type_service"])


# UPDATE
def test_update_type_service(
    client: TestClient,
    superuser_token_headers: dict,
):
    type_service2 = data["type_service"][1]
    type_service_data = TypeServiceUpdate(
        name=fake.name().upper(), key=fake.name().upper().replace(" ", "_")
    ).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/type_service/update_by_id/{type_service2['id']}",
        headers=superuser_token_headers,
        json=type_service_data,
    )
    assert r.status_code == 200
    updated_type_service = r.json()
    assert updated_type_service["name"] == type_service_data["name"]
    assert updated_type_service["key"] == type_service_data["key"]
    # Revert the changes
    rollback_data = TypeServiceUpdate(
        name=type_service2["name"], key=type_service2["key"]
    ).model_dump()
    type_service_services.update_type_service(
        id=type_service2["id"], data=rollback_data
    )


def test_update_type_service_duplicate(
    client: TestClient,
    superuser_token_headers: dict,
):
    type_service1 = data["type_service"][0]
    type_service2 = data["type_service"][1]
    type_service_data = TypeServiceUpdate(name=type_service2["name"]).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/type_service/update_by_id/{type_service1['id']}",
        headers=superuser_token_headers,
        json=type_service_data,
    )
    assert r.status_code == 400
    assert (
        r.json()["detail"] == "Name already used"
        or r.json()["detail"] == "Key already used"
    )


def test_update_type_service_no_permission(
    client: TestClient,
    normal_user_token_headers: dict,
):
    type_service2 = data["type_service"][1]
    type_service_data = TypeServiceUpdate(
        name="William Bray1", key="Karen Miller1"
    ).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/type_service/update_by_id/{type_service2['id']}",
        headers=normal_user_token_headers,
        json=type_service_data,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Not enough permissions"


def test_update_type_service_not_found(
    client: TestClient,
    superuser_token_headers: dict,
):
    type_service_data = TypeServiceUpdate(
        name="William Bray1", key="Karen Miller1"
    ).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/type_service/update_by_id/66372d0de0efbcb3d9b331b5",
        headers=superuser_token_headers,
        json=type_service_data,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Type service not found"


# DELETE
def test_delete_type_service(
    client: TestClient,
    superuser_token_headers: dict,
):
    fake = Faker()
    type_service_data = TypeServiceCreate(
        name=fake.name(),  # Generate a random
        key=fake.name(),  # Generate a random
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/type_service/create",
        headers=superuser_token_headers,
        json=type_service_data,
    )
    assert r.status_code == 201
    created_type_service = r.json()
    assert created_type_service["name"] == type_service_data["name"]
    assert created_type_service["key"] == type_service_data["key"]

    r = client.delete(
        f"{settings.API_V1_STR}/type_service/delete_by_id/{created_type_service['id']}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert r.json()["msg"] == "Type service deleted"


def test_delete_type_service_not_found(
    client: TestClient,
    superuser_token_headers: dict,
):
    r = client.delete(
        f"{settings.API_V1_STR}/type_service/delete_by_id/66372d0de0efbcb3d9b331b5",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Not found"
