from fastapi.testclient import TestClient
from faker import Faker

from app.core.config import settings
from app.schemas.webhook_schemas import WebhookCreate, WebhookUpdate
from app.services import webhook_services
from app.services import user_services
from app.tests.init_db import init_data as data

fake = Faker()


def test_create_webhook(
    client: TestClient,
    superuser_token_headers: dict,
):
    type_service1 = data["type_service"][0]
    webhook_data = WebhookCreate(
        name=fake.company(),  # Generate a random company name
        endpoint=fake.uri(),  # Generate a random uri
        type_service_id=type_service1["id"],
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/webhook/create",
        headers=superuser_token_headers,
        json=webhook_data,
    )
    assert r.status_code == 201
    created_webhook = r.json()
    assert created_webhook["endpoint"] == webhook_data["endpoint"]
    assert created_webhook["type_service"]["id"] == type_service1["id"]
    # revert the changes
    try:
        webhook_services.remove(id=created_webhook["id"])
    except Exception as e:
        assert False, f"Error: {e}"


def test_create_webhook_duplicate(
    client: TestClient,
    superuser_token_headers: dict,
):
    webhook1 = data["webhook"][0]
    webhook_data = WebhookCreate(
        name=webhook1["name"],
        endpoint=webhook1["endpoint"],
        type_service_id=data["type_service"][0]["id"],
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/webhook/create",
        headers=superuser_token_headers,
        json=webhook_data,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Webhook already used"


def test_get_webhooks(
    client: TestClient,
    superuser_token_headers: dict,
):
    r = client.get(
        f"{settings.API_V1_STR}/webhook/get_all",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    webhooks = r.json()["data"]
    assert webhooks
    for webhook in webhooks:
        assert "name" in webhook
        assert "endpoint" in webhook


def test_get_webhook_by_id(
    client: TestClient,
    superuser_token_headers: dict,
):
    webhook1 = data["webhook"][0]
    r = client.get(
        f"{settings.API_V1_STR}/webhook/get_by_id/{webhook1['id']}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    webhook = r.json()
    assert webhook
    assert webhook["id"] == webhook1["id"]
    assert webhook["name"] == webhook1["name"]
    assert webhook["endpoint"] == webhook1["endpoint"]
    assert webhook["type_service"]["id"] == webhook1["type_service"]
    assert webhook["company"] == webhook1["company"]


def test_update_webhook_by_id(
    client: TestClient,
    normal_user2_token_headers: dict,
):
    """Test update webhook 2 by id, it associated with company 2, normal user 2"""
    webhook2 = data["webhook"][1]
    webhook_data = WebhookUpdate(
        name=fake.company(),  # Generate a random company name
        endpoint=fake.uri(),  # Generate a random uri
    ).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/webhook/update_by_id/{webhook2['id']}",
        headers=normal_user2_token_headers,
        json=webhook_data,
    )
    assert r.status_code == 200
    updated_webhook = r.json()
    assert updated_webhook["name"] == webhook_data["name"]
    assert updated_webhook["endpoint"] == webhook_data["endpoint"]
    # revert the changes
    user = user_services.get(id=data["normal_user"][1]["id"])
    data_in = {
        "name": data["webhook"][1]["name"],
        "endpoint": data["webhook"][1]["endpoint"],
    }
    webhook_services.update_webhook(user=user, id=webhook2["id"], obj_in=data_in)


def test_delete_webhook_by_id(
    client: TestClient,
    normal_user2_token_headers: dict,
):
    type_service2 = data["type_service"][1]
    webhook_data = WebhookCreate(
        name=fake.company(),
        endpoint=fake.uri(),
        type_service_id=type_service2["id"],
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/webhook/create",
        headers=normal_user2_token_headers,
        json=webhook_data,
    )
    assert r.status_code == 201
    created_webhook = r.json()
    assert created_webhook["endpoint"] == webhook_data["endpoint"]
    assert created_webhook["type_service"]["id"] == type_service2["id"]
    r = client.delete(
        f"{settings.API_V1_STR}/webhook/delete_by_id/{created_webhook['id']}",
        headers=normal_user2_token_headers,
    )
    assert r.status_code == 200
    assert r.json()["msg"] == "Webhook deleted"


def test_delete_webhook_by_id_not_found(
    client: TestClient,
    normal_user_token_headers: dict,
):
    r = client.delete(
        f"{settings.API_V1_STR}/webhook/delete_by_id/{data['fake_id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Not found"


def test_get_by_company_and_type_service():
    company1 = data["company"][0]
    type_service1 = data["type_service"][0]
    webhooks = webhook_services.get_by_company_and_type_service(
        company_id=company1["id"], type_service_id=type_service1["id"]
    )
    assert webhooks
    for webhook in webhooks:
        assert str(webhook.company.id) == company1["id"]
        assert str(webhook.type_service.id) == type_service1["id"]
