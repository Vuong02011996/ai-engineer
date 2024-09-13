from fastapi.testclient import TestClient
from faker import Faker

from app.schemas.brand_camera_schemas import BrandCameraCreate, BrandCameraUpdate
from app.core.config import settings
from app.tests.init_db import init_data as data
from app.services import brand_camera_services

fake = Faker()


def test_create_brand_camera(
    client: TestClient,
    superuser_token_headers: dict,
):
    fake_name = fake.company()
    brand_camera_data = BrandCameraCreate(
        name=fake_name,
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/brand_camera/create",
        headers=superuser_token_headers,
        json=brand_camera_data,
    )
    assert r.status_code == 201
    brand_camera = r.json()
    assert brand_camera
    assert brand_camera["name"] == fake_name
    # Delete brand camera
    brand_camera_services.remove(id=brand_camera["id"])


def test_create_brand_camera_duplicate(
    client: TestClient,
    superuser_token_headers: dict,
):
    brand_camera_data = BrandCameraCreate(
        name=data["brand_camera"][0]["name"],
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/brand_camera/create",
        headers=superuser_token_headers,
        json=brand_camera_data,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Brand Camera already exists"


def test_get_all_brand_camera(
    client: TestClient,
):
    r = client.get(
        f"{settings.API_V1_STR}/brand_camera/get_all",
    )
    assert r.status_code == 200
    brand_cameras = r.json()["data"]
    assert brand_cameras
    assert len(brand_cameras) == len(data["brand_camera"])
    for brand_camera in brand_cameras:
        assert brand_camera["id"]
        assert brand_camera["name"]


def test_get_brand_camera_by_id(
    client: TestClient,
):
    brand_camera_id = data["brand_camera"][0]["id"]
    r = client.get(
        f"{settings.API_V1_STR}/brand_camera/get_by_id/{brand_camera_id}",
    )
    assert r.status_code == 200
    brand_camera = r.json()
    assert brand_camera
    assert brand_camera["id"] == brand_camera_id
    assert brand_camera["name"] == data["brand_camera"][0]["name"]


def test_get_brand_camera_by_id_not_found(
    client: TestClient,
):
    r = client.get(
        f"{settings.API_V1_STR}/brand_camera/get_by_id/{data['fake_id']}",
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Brand Camera not found"


def test_count_brand(client: TestClient):
    r = client.get(
        f"{settings.API_V1_STR}/brand_camera/count",
    )
    assert r.status_code == 200
    response = r.json()
    assert response["count"] == len(data["brand_camera"])


def test_update_brand_camera(
    client: TestClient,
    superuser_token_headers: dict,
):
    brand_camera_id1 = data["brand_camera"][0]["id"]
    fake_name = fake.company()
    brand_camera_data = BrandCameraUpdate(
        name=fake_name,
    ).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/brand_camera/update_by_id/{brand_camera_id1}",
        json=brand_camera_data,
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    brand_camera = r.json()
    assert brand_camera
    assert brand_camera["name"] == fake_name
    # Reset brand camera name
    brand_camera_services.update_brand_camera(
        id=brand_camera_id1,
        obj_in=BrandCameraUpdate(name=data["brand_camera"][0]["name"]),
    )


def test_update_brand_camera_duplicate(client: TestClient, superuser_token_headers):
    brand_camera_id1 = data["brand_camera"][0]["id"]
    brand_camera_data = BrandCameraUpdate(
        name=data["brand_camera"][1]["name"],
    ).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/brand_camera/update_by_id/{brand_camera_id1}",
        json=brand_camera_data,
        headers=superuser_token_headers,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Brand Camera name already used"


def test_update_brand_camera_not_found(
    client: TestClient,
    superuser_token_headers: dict,
):
    brand_camera_data = BrandCameraUpdate(
        name=fake.company(),
    ).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/brand_camera/update_by_id/{data['fake_id']}",
        json=brand_camera_data,
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Brand Camera not found"


def test_delete_brand_camera(
    client: TestClient,
    superuser_token_headers: dict,
):
    brand_in = BrandCameraCreate(name=fake.company())
    brand_camera = brand_camera_services.create_brand_camera(obj_in=brand_in)
    r = client.delete(
        f"{settings.API_V1_STR}/brand_camera/delete_by_id/{brand_camera.id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    response = r.json()
    assert response
    assert response["msg"] == "Brand Camera deleted"


def test_delete_brand_camera_not_found(
    client: TestClient,
    superuser_token_headers: dict,
):
    r = client.delete(
        f"{settings.API_V1_STR}/brand_camera/delete/6637135e4b0e6af194e68384",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Not Found"
