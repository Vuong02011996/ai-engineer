from fastapi.testclient import TestClient
from faker import Faker

from app.core.config import settings
from app.schemas.server_schemas import ServerCreate, ServerUpdate
from app.tests.init_db import init_data as data

fake = Faker()


# CREATE
def test_create_and_delete_server(
    client: TestClient,
    superuser_token_headers: dict,
    normal_user_token_headers: dict,
):
    server_data = ServerCreate(
        name=fake.company(),  # Generate a random company name
        ip_address=fake.ipv4_private(),  # Generate a random domain name
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/server/create",
        headers=superuser_token_headers,
        json=server_data,
    )
    assert r.status_code == 201
    created_server = r.json()
    assert created_server["name"] == server_data["name"]
    assert created_server["ip_address"] == server_data["ip_address"]
    # Clean up
    r = client.delete(
        f"{settings.API_V1_STR}/server/delete_by_id/{created_server['id']}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert r.json() == {"msg": "Server deleted"}
    # Check if the server was deleted
    r = client.get(
        f"{settings.API_V1_STR}/server/get_by_id/{created_server['id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Server not found"


def test_create_server_no_permission(
    client: TestClient,
    normal_user_token_headers: dict,
):
    server_data = ServerCreate(
        name=fake.company(),  # Generate a random company name
        ip_address=fake.ipv4_public(),  # Generate a random domain name
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/server/create",
        headers=normal_user_token_headers,
        json=server_data,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Not enough permissions"


def test_create_server_duplicate_ip(
    client: TestClient,
    superuser_token_headers: dict,
):
    server_oryza = data["server"][0]
    server_create = ServerCreate(
        name=fake.name(), ip_address=server_oryza["ip_address"]
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/server/create",
        headers=superuser_token_headers,
        json=server_create,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "IP address already used"


def test_create_server_duplicate_name(
    client: TestClient,
    superuser_token_headers: dict,
):
    server1 = data["server"][0]
    server_data = ServerCreate(
        name=server1["name"], ip_address=fake.ipv4_public()
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/server/create",
        headers=superuser_token_headers,
        json=server_data,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Name already used"


# GET
def test_get_servers(
    client: TestClient,
    superuser_token_headers: dict,
):
    r = client.get(
        f"{settings.API_V1_STR}/server/get_all",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    servers = r.json()["data"]
    assert servers
    for server in servers:
        assert "name" in server
        assert "ip_address" in server
        assert "is_alive" in server


def test_get_server_by_id(
    client: TestClient,
    normal_user_token_headers: dict,
):
    server1 = data["server"][0]
    r = client.get(
        f"{settings.API_V1_STR}/server/get_by_id/{server1['id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    server = r.json()
    assert server
    assert server["name"] == server1["name"]
    assert server["ip_address"] == server1["ip_address"]
    assert server["is_alive"] == server1["is_alive"]


def test_get_server_by_id_not_found(
    client: TestClient,
    superuser_token_headers: dict,
):
    server_id = "66312c944e3b9c2b03b8f1b7"
    r = client.get(
        f"{settings.API_V1_STR}/server/get_by_id/{server_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Server not found"


def test_count_servers(
    client: TestClient,
    superuser_token_headers: dict,
):
    """Test counting the number of servers."""
    r = client.get(
        f"{settings.API_V1_STR}/server/count",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert r.json()["count"] == len(data["server"])


# UPDATE
def test_update_server_by_id(client: TestClient, superuser_token_headers: dict):
    """Test updating a server's IP address."""
    server2 = data["server"][1]
    new_ip_address = fake.ipv4()
    update_data = ServerUpdate(ip_address=new_ip_address).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/server/update_by_id/{server2['id']}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert r.status_code == 200
    updated_server = r.json()
    assert updated_server["ip_address"] == new_ip_address
    # Reset the server's IP address
    update_data = ServerUpdate(ip_address=server2["ip_address"]).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/server/update_by_id/{server2['id']}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert r.status_code == 200
    updated_server = r.json()
    assert updated_server["ip_address"] == server2["ip_address"]


def test_update_server_by_id_not_found(
    client: TestClient,
    superuser_token_headers: dict,
):
    """Test updating a server that does not exist."""
    fake_server_id = "6636789a5daf7f01ee9fad22"
    update_data = ServerUpdate(ip_address=fake.ipv4()).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/server/update_by_id/{fake_server_id}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Server not found"


def test_update_server_no_permission(
    client: TestClient,
    normal_user_token_headers: dict,
):
    """Normal user should not be able to update a server."""
    server_id = data["server"][1]["id"]
    update_data = ServerUpdate(ip_address=fake.ipv4()).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/server/update_by_id/{server_id}",
        headers=normal_user_token_headers,
        json=update_data,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Not enough permissions"


def test_update_server_by_id_duplicate_ip(
    client: TestClient, superuser_token_headers: dict
):
    """Test updating a server with an IP address that is already used."""
    server2 = data["server"][1]
    server1 = data["server"][0]
    update_data = ServerUpdate(ip_address=server1["ip_address"]).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/server/update_by_id/{server2['id']}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "IP address already used"


def test_delete_server_by_id_not_found(
    client: TestClient,
    superuser_token_headers: dict,
):
    """Test deleting a server that does not exist."""
    fake_server_id = "6636789a5daf7f01ee9fad22"
    r = client.delete(
        f"{settings.API_V1_STR}/server/delete_by_id/{fake_server_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Not found"


def test_delete_server_no_permission(
    client: TestClient,
    normal_user_token_headers: dict,
):
    """Normal user should not be able to delete a server."""
    server_id = data["server"][1]["id"]
    r = client.delete(
        f"{settings.API_V1_STR}/server/delete_by_id/{server_id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Not enough permissions"
