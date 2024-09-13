from fastapi.testclient import TestClient
from faker import Faker

from app.core.config import settings
from app.schemas.service_schemas import ServiceCreate, ServiceUpdate
from app.tests.init_db import init_data as data
from app.services import service_services

fake = Faker()


def test_create_service(
    client: TestClient,
    superuser_token_headers: dict,
):
    type_service2 = data["type_service"][1]
    server2 = data["server"][1]
    service_create = ServiceCreate(
        name=fake.company(),
        port=str(fake.port_number()),
        max_process=fake.random_int(min=1, max=10),
        type_service_id=type_service2["id"],
        server_id=server2["id"],
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/service/create",
        headers=superuser_token_headers,
        json=service_create,
    )
    assert r.status_code == 201
    created_service = r.json()
    assert created_service["name"] == service_create["name"]
    assert created_service["port"] == service_create["port"]
    assert created_service["max_process"] == service_create["max_process"]
    assert created_service["type_service"] == type_service2["id"]
    assert created_service["server"] == server2["id"]
    assert "id" in created_service
    # Clean up
    service_services.remove(id=created_service["id"])


def test_create_service_invalid_field(
    client: TestClient,
    superuser_token_headers: dict,
):
    service_data = ServiceCreate(
        name=fake.company(),
        port=str(fake.port_number()),
        max_process=fake.random_int(min=1, max=10),
        type_service_id=data["fake_id"],
        server_id=data["fake_id"],
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/service/create",
        headers=superuser_token_headers,
        json=service_data,
    )
    assert (
        r.status_code == 404
        and (
            r.json()["detail"] == "Type service not found"
            or r.json()["detail"] == "Server not found"
        )
    ) or (r.status_code == 400 and r.json()["detail"] == "Invalid ID")


def test_create_service_duplicate(
    client: TestClient,
    superuser_token_headers: dict,
):
    type_service1 = data["type_service"][0]
    server1 = data["server"][0]
    service1 = data["service"][0]
    # type_service1 and server1 and service1 are associated
    service_data = ServiceCreate(
        name=fake.company(),
        port=service1["port"],
        max_process=1,
        type_service_id=type_service1["id"],
        server_id=server1["id"],
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/service/create",
        headers=superuser_token_headers,
        json=service_data,
    )
    assert r.status_code == 400 and (
        r.json()["detail"] == "Name already used"
        or r.json()["detail"] == "Port service already used"
    )


def test_get_services(
    client: TestClient,
    normal_user_token_headers: dict,
):
    r = client.get(
        f"{settings.API_V1_STR}/service/get_all",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    services = r.json()
    assert services
    services = services["data"]
    for service in services:
        assert "id" in service
        assert "name" in service
        assert "port" in service
        assert "max_process" in service
        assert "type_service" in service
        assert "server" in service
    assert len(services) == len(data["service"])


def test_get_service_by_id(
    client: TestClient,
    normal_user_token_headers: dict,
):
    service1 = data["service"][0]
    r = client.get(
        f"{settings.API_V1_STR}/service/get_by_id/{service1['id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    service = r.json()
    assert service
    assert service["id"] == service1["id"]
    assert service["name"] == service1["name"]
    assert service["port"] == service1["port"]
    assert service["max_process"] == service1["max_process"]
    assert service["type_service"] == service1["type_service"]
    assert service["server"] == service1["server"]


def test_delete_service_by_id(
    client: TestClient,
    superuser_token_headers: dict,
):
    type_service1 = data["type_service"][0]
    server1 = data["server"][0]
    service_data = ServiceCreate(
        name=fake.company(),  # Generate a random company name
        port=str(fake.port_number()),  # Generate a random port number
        max_process=fake.random_int(
            min=1, max=10
        ),  # Generate a random max process number
        type_service_id=type_service1["id"],
        server_id=server1["id"],
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/service/create",
        headers=superuser_token_headers,
        json=service_data,
    )
    assert r.status_code == 201
    created_service = r.json()
    assert created_service["name"] == service_data["name"]
    assert created_service["port"] == service_data["port"]
    assert created_service["max_process"] == service_data["max_process"]
    assert created_service["type_service"] == type_service1["id"]
    assert created_service["server"] == server1["id"]
    # Clean up
    r = client.delete(
        f"{settings.API_V1_STR}/service/delete_by_id/{created_service['id']}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert r.json()["msg"] == "Service deleted"


def test_update_service(
    client: TestClient,
    superuser_token_headers: dict,
):
    service1 = data["service"][0]
    service_data = ServiceUpdate(
        name=fake.company(),
        port=str(fake.port_number()),
        max_process=fake.random_int(min=1, max=10),
    ).model_dump()
    print("service_data", service_data)
    r = client.put(
        f"{settings.API_V1_STR}/service/update_by_id/{service1['id']}",
        headers=superuser_token_headers,
        json=service_data,
    )
    assert r.status_code == 200
    updated_service = r.json()
    assert updated_service["name"] == service_data["name"]
    assert updated_service["port"] == service_data["port"]
    assert updated_service["max_process"] == service_data["max_process"]
    # revert the changes
    revert_data = ServiceUpdate(
        name=service1["name"],
        port=service1["port"],
        max_process=service1["max_process"],
    )  # Call by function is different from call by api route, api -> json, function -> dict
    print("revert_data", revert_data)
    service_services.update_service(id=service1["id"], data=revert_data)


def test_update_service_2(
    client: TestClient,
    superuser_token_headers: dict,
):
    service1 = data["service"][0]
    update_data = ServiceUpdate(
        type_service_id=data["type_service"][0]["id"],
        server_id=data["server"][0]["id"],
    ).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/service/update_by_id/{service1['id']}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert r.status_code == 200
    updated_service = r.json()
    assert updated_service["type_service"] == data["type_service"][0]["id"]
    assert updated_service["server"] == data["server"][0]["id"]

    # revert the changes
    revert_data = ServiceUpdate(
        type_service_id=service1["type_service"],
        server_id=service1["server"],
    )
    service_services.update_service(id=service1["id"], data=revert_data)


def test_update_service_invalid_field(
    client: TestClient,
    superuser_token_headers: dict,
):
    service1 = data["service"][0]
    update_data = ServiceUpdate(
        type_service_id=data["fake_id"],
        server_id=data["fake_id"],
    ).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/service/update_by_id/{service1['id']}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert (
        r.status_code == 404
        and (
            r.json()["detail"] == "Type service not found"
            or r.json()["detail"] == "Server not found"
        )
    ) or (r.status_code == 400 and r.json()["detail"] == "Invalid ID")
    # revert the changes
    revert_data = ServiceUpdate(
        type_service_id=service1["type_service"],
        server_id=service1["server"],
    )
    service_services.update_service(id=service1["id"], data=revert_data)
