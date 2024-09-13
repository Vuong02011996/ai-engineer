from fastapi.testclient import TestClient
from faker import Faker

from app.core.config import settings
from app.schemas.camera_schemas import CameraCreate, CameraUpdate
from app.services import camera_services, user_services
from app.tests.init_db import init_data as data

fake = Faker()


# CREATE
def test_create_camera(
    client: TestClient,
    normal_user_token_headers: dict,
):
    camera_data = CameraCreate(
        name=fake.company(),  # Generate a random company name
        ip_address=fake.ipv4_private(),  # Generate a random domain name
        port=str(fake.port_number()),  # Generate a random port number
        username=fake.user_name(),  # Generate a random username
        password=fake.password(),  # Generate a random password
        rtsp=fake.uri(),  # Generate a random rtsp
        brand_camera_id=data["brand_camera"][0]["id"],  # Generate a random company name
        is_ai=True,
        other_info={},
        type_service_ids=[data["service"][0]["id"], data["service"][1]["id"]]
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/camera/create",
        headers=normal_user_token_headers,
        json=camera_data,
    )
    assert r.status_code == 201
    created_camera = r.json()
    assert created_camera["name"] == camera_data["name"]
    assert created_camera["ip_address"] == camera_data["ip_address"]
    assert created_camera["port"] == camera_data["port"]
    assert created_camera["username"] == camera_data["username"]
    assert created_camera["password"] == camera_data["password"]
    assert created_camera["rtsp"] == camera_data["rtsp"]
    assert created_camera["brand_camera"] == camera_data["brand_camera_id"]
    assert created_camera["is_ai"] == camera_data["is_ai"]
    assert created_camera["other_info"] == camera_data["other_info"]
    # Delete camera
    camera_services.remove(id=created_camera["id"])


def test_create_camera_duplicate(
    client: TestClient,
    normal_user_token_headers: dict,
):
    camera1 = data["camera"][0]
    camera_data = CameraCreate(
        name=fake.company(),  # Generate a random company name
        ip_address=camera1["ip_address"],  # Generate a random domain name
        port=str(camera1["port"]),  # Generate a random port number
        username=fake.user_name(),  # Generate a random username
        password=fake.password(),  # Generate a random password
        rtsp=fake.uri(),  # Generate a random rtsp
        brand_camera_id=data["brand_camera"][0]["id"],  # Generate a random company name
        is_ai=True,
        other_info={},
        type_service_ids=[]
    ).model_dump()
    print(camera_data)
    r = client.post(
        f"{settings.API_V1_STR}/camera/create",
        headers=normal_user_token_headers,
        json=camera_data,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Camera already exists"


# READ
def test_count_camera(
    client: TestClient,
    normal_user_token_headers: dict,
):
    r = client.get(
        f"{settings.API_V1_STR}/camera/count",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    response = r.json()
    assert response["count"] > 0


def test_get_cameras(
    client: TestClient,
    normal_user_token_headers: dict,
):
    r = client.get(
        f"{settings.API_V1_STR}/camera/get_all",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    cameras = r.json()["data"]
    assert cameras
    for camera in cameras:
        assert "name" in camera
        assert "ip_address" in camera
        assert "port" in camera
        assert "username" in camera
        assert "password" in camera
        assert "rtsp" in camera
        assert "brand_camera" in camera
        assert "is_ai" in camera
        assert "other_info" in camera


def test_get_camera_by_id(
    client: TestClient,
    normal_user_token_headers: dict,
):
    camera_id = data["camera"][0]["id"]
    r = client.get(
        f"{settings.API_V1_STR}/camera/get_by_id/{camera_id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    camera = r.json()
    assert camera
    assert camera["name"] == "OryzaRDBT"
    assert camera["ip_address"] == "192.168.111.6"
    assert camera["port"] == 80
    assert camera["username"] == "admin"
    assert camera["password"] == "Oryza@123"
    assert camera["rtsp"] == "rtsp://"


def test_get_camera_by_id_not_found(
    client: TestClient,
    normal_user_token_headers: dict,
):
    r = client.get(
        f"{settings.API_V1_STR}/camera/get_by_id/6637135e4b0e6af194e68384",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Camera not found"


def test_get_cameras_by_company_id(
    client: TestClient,
    normal_user_token_headers: dict,
):
    company_id = data["company"][0]["id"]
    r = client.get(
        f"{settings.API_V1_STR}/camera/get_by_company_id/{company_id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    cameras = r.json()["data"]
    assert cameras
    for camera in cameras:
        assert "name" in camera
        assert "ip_address" in camera
        assert "port" in camera
        assert "username" in camera
        assert "password" in camera
        assert "rtsp" in camera


# UPDATE
def test_update_camera(
    client: TestClient,
    normal_user_token_headers: dict,
):
    camera_id = data["camera"][0]["id"]
    new_name = "Oryza3"
    update_data = CameraUpdate(
        name=new_name,
    )
    r = client.put(
        f"{settings.API_V1_STR}/camera/update_by_id/{camera_id}",
        headers=normal_user_token_headers,
        json=update_data.model_dump(),
    )
    assert r.status_code == 200
    updated_camera = r.json()
    assert updated_camera["name"] == new_name
    # Revert changes
    update_data = CameraUpdate(
        name=data["camera"][0]["name"],
    )
    r = client.put(
        f"{settings.API_V1_STR}/camera/update_by_id/{camera_id}",
        headers=normal_user_token_headers,
        json=update_data.model_dump(),
    )
    assert r.status_code == 200
    updated_camera = r.json()
    assert updated_camera["name"] == data["camera"][0]["name"]


def test_update_camera_ip_address_duplicate(
    client: TestClient,
    normal_user_token_headers: dict,
):
    camera1 = data["camera"][0]
    camera2 = data["camera"][1]
    update_data = CameraUpdate(ip_address=camera2["ip_address"])
    r = client.put(
        f"{settings.API_V1_STR}/camera/update_by_id/{camera1['id']}",
        headers=normal_user_token_headers,
        json=update_data.model_dump(),
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "IP address already used"


def test_update_camera_not_found(
    client: TestClient,
    normal_user_token_headers: dict,
):
    update_data = CameraUpdate(
        name="OryzaRD",
    )
    r = client.put(
        f"{settings.API_V1_STR}/camera/update_by_id/6637135e4b0e6af194e68384",
        headers=normal_user_token_headers,
        json=update_data.model_dump(),
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Camera not found"


# DELETE
def test_delete_camera(
    client: TestClient,
    normal_user_token_headers: dict,
):
    camera_data = CameraCreate(
        name=fake.company(),  # Generate a random company name
        ip_address=fake.ipv4_private(),  # Generate a random domain name
        port=str(fake.port_number()),  # Generate a random port number
        username=fake.user_name(),  # Generate a random username
        password=fake.password(),  # Generate a random password
        rtsp=fake.uri(),  # Generate a random rtsp
        brand_camera_id=data["brand_camera"][0]["id"],  # Generate a random company name
        is_ai=True,
        other_info={},
        type_service_ids=[]
    )
    user = user_services.get(id=data["normal_user"][0]["id"])
    created_camera = camera_services.create_camera(
        user=user, obj_in=camera_data
    ).model_dump()

    r = client.delete(
        f"{settings.API_V1_STR}/camera/delete_by_id/{created_camera['id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    r = client.get(
        f"{settings.API_V1_STR}/camera/get_by_id/{str(created_camera['id'])}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Camera not found"


def test_delete_camera_not_found(
    client: TestClient,
    normal_user_token_headers: dict,
):
    r = client.delete(
        f"{settings.API_V1_STR}/camera/delete_by_id/{data['fake_id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Not found"
