from fastapi.testclient import TestClient
from faker import Faker

from app.core.config import settings
from app.schemas.process_schemas import ProcessCreate
from app.tests.init_db import init_data as data
from app.services import process_services

fake = Faker()


def test_run_kill_process(
    client: TestClient,
    normal_user_token_headers: dict,
):
    process_data = {
        "process_id": data["process"][0]["id"],
    }
    r = client.post(
        f"{settings.API_V1_STR}/process/run",
        headers=normal_user_token_headers,
        json=process_data,
    )
    assert r.status_code == 200  # TODO: fix process to return code 200 later
    created_process = r.json()
    assert created_process["camera"] == data["process"][0]["camera"]
    assert created_process["service"]["id"] == data["process"][0]["service"]

    # Kill the process
    r = client.post(
        f"{settings.API_V1_STR}/process/kill/{created_process['id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200


def test_create_delete_process(
    client: TestClient,
    normal_user2_token_headers: dict,
):
    process_data = ProcessCreate(
        service_id=data["service"][1]["id"],
        camera_id=data["camera"][1]["id"],
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/process/create",
        headers=normal_user2_token_headers,
        json=process_data,
    )
    assert r.status_code == 201

    created_process = r.json()
    assert created_process["service"]["id"] == process_data["service_id"]
    assert created_process["camera"] == process_data["camera_id"]
    # Clean up
    process_services.remove(id=created_process["id"])


def test_create_process_duplicate(
    client: TestClient,
    normal_user_token_headers: dict,
):
    # There are two processes in the database, one with camera 1, service 1, one with camera 1, service 2
    process_data = ProcessCreate(
        service_id=data["service"][0]["id"],
        camera_id=data["camera"][0]["id"],
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/process/create",
        headers=normal_user_token_headers,
        json=process_data,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Process already exists"


def test_delete_not_found_process(
    client: TestClient,
    superuser_token_headers: dict,
):
    r = client.delete(
        f"{settings.API_V1_STR}/process/delete_by_id/{data['fake_id']}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Not found"


def test_get_processes(
    client: TestClient,
    normal_user_token_headers: dict,
):
    r = client.get(
        f"{settings.API_V1_STR}/process/get_all",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    processes = r.json()["data"]
    assert processes
    for process in processes:
        assert "service" in process
        assert "camera" in process
        assert "status" in process
        assert "pid" in process


def test_get_process_by_id(client: TestClient, normal_user_token_headers: dict):
    r = client.get(
        f"{settings.API_V1_STR}/process/get_by_id/{data['process'][0]['id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    process = r.json()
    assert process["id"] == data["process"][0]["id"]
    assert process["service"]["id"] == data["process"][0]["service"]
    assert process["camera"] == data["process"][0]["camera"]
    assert process["status"] is not None
    assert process["pid"] is not None


def test_get_process_by_id_not_found(
    client: TestClient, normal_user_token_headers: dict
):
    r = client.get(
        f"{settings.API_V1_STR}/process/get_by_id/{data['fake_id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Process not found"


def test_get_process_by_camera_id(client: TestClient, normal_user_token_headers: dict):
    r = client.get(
        f"{settings.API_V1_STR}/process/get_by_camera_id/{data['camera'][0]['id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    processes = r.json()["data"]
    assert processes
    cameras = [data["camera"][0]["id"], data["camera"][1]["id"]]
    for process in processes:
        assert process["camera"] in cameras


def test_update_by_id(client: TestClient, normal_user_token_headers: dict):
    process_data = {
        # "service_id": data["service"][1]["id"],
        "status": "START",
    }
    r = client.put(
        f"{settings.API_V1_STR}/process/update_by_id/{data['process'][0]['id']}",
        headers=normal_user_token_headers,
        json=process_data,
    )
    assert r.status_code == 200
    updated_process = r.json()
    print(updated_process)
    # assert updated_process["service"]["id"] == process_data["service_id"]
    assert updated_process["status"] == process_data["status"]
    # Revert back
    process = process_services.get(id=data["process"][0]["id"])
    process_services.update(
        db_obj=process, obj_in={"service_id": data["process"][0]["service"]}
    )
