from fastapi.testclient import TestClient
from faker import Faker

from app.core.config import settings
from app.schemas.company_schemas import CompanyCreate
from app.services import company_services

fake = Faker()


def test_create_company(
    client: TestClient,
    superuser_token_headers: dict,
):
    fake = Faker()
    company_data = CompanyCreate(
        name=fake.company(),  # Generate a random company name
        domain=fake.domain_name(),  # Generate a random domain name
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/company/create",
        headers=superuser_token_headers,
        json=company_data,
    )
    assert r.status_code == 201
    created_company = r.json()
    assert created_company["name"] == company_data["name"]
    assert created_company["domain"] == company_data["domain"]
    # Clean up
    company_services.remove(id=created_company["id"])


def test_create_company_duplicate(
    client: TestClient,
    superuser_token_headers: dict,
):
    company_data = CompanyCreate(name="Oryza", domain="oryza.vn").model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/company/create",
        headers=superuser_token_headers,
        json=company_data,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Company already exists"


def test_get_companies(
    client: TestClient,
):
    r = client.get(
        f"{settings.API_V1_STR}/company/get_all",
    )
    assert r.status_code == 200
    companies = r.json()["data"]
    assert companies
    for company in companies:
        assert "name" in company
        assert "domain" in company


def test_get_my_company(
    client: TestClient,
    normal_user_token_headers: dict,
):
    r = client.get(
        f"{settings.API_V1_STR}/company/get_my_company",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    company = r.json()
    assert company
    assert company["name"] == "Oryza"
    assert company["domain"] == "oryza.vn"


def test_get_company_by_id(
    client: TestClient,
):
    company_id = company_services.get_company_by_name(name="Oryza").id
    r = client.get(
        f"{settings.API_V1_STR}/company/get_by_id/{str(company_id)}",
    )
    assert r.status_code == 200
    company = r.json()
    assert company
    assert company["name"] == "Oryza"
    assert company["domain"] == "oryza.vn"


def test_get_company_by_id_not_found(
    client: TestClient,
):
    r = client.get(
        f"{settings.API_V1_STR}/company/get_by_id/60f6e4b1c2b1f7d2c7e3f6c1",
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Company not found"


def test_count_company(
    client: TestClient,
):
    r = client.get(
        f"{settings.API_V1_STR}/company/count",
    )
    assert r.status_code == 200
    assert r.json()["count"] >= 0


def test_update_company(
    client: TestClient,
    superuser_token_headers: dict,
):
    fake = Faker()
    company_data = CompanyCreate(
        name=fake.company(),  # Generate a random company name
        domain=fake.domain_name(),  # Generate a random domain name
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/company/create",
        headers=superuser_token_headers,
        json=company_data,
    )
    assert r.status_code == 201
    created_company = r.json()
    assert created_company["name"] == company_data["name"]
    assert created_company["domain"] == company_data["domain"]

    company_data["name"] = fake.company()
    company_data["domain"] = fake.domain_name()

    r = client.put(
        f"{settings.API_V1_STR}/company/update_by_id/{created_company['id']}",
        headers=superuser_token_headers,
        json=company_data,
    )
    assert r.status_code == 200
    updated_company = r.json()
    assert updated_company["name"] == company_data["name"]
    assert updated_company["domain"] == company_data["domain"]


def test_update_company_duplicate(
    client: TestClient,
    superuser_token_headers: dict,
):
    company_data = CompanyCreate(
        name=fake.company(),  # Generate a random company name
        domain=fake.url(),  # Generate a random domain name
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/company/create",
        headers=superuser_token_headers,
        json=company_data,
    )
    assert r.status_code == 201
    created_company = r.json()
    assert created_company["name"] == company_data["name"]
    assert created_company["domain"] == company_data["domain"]
    company_data["name"] = "Oryza"
    r = client.put(
        f"{settings.API_V1_STR}/company/update_by_id/{created_company['id']}",
        headers=superuser_token_headers,
        json=company_data,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Company with this name already exists"


# DELETE
def test_delete_company(
    client: TestClient,
    superuser_token_headers: dict,
):
    fake = Faker()
    company_data = CompanyCreate(
        name=fake.company(),  # Generate a random company name
        domain=fake.domain_name(),  # Generate a random domain name
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/company/create",
        headers=superuser_token_headers,
        json=company_data,
    )
    assert r.status_code == 201
    created_company = r.json()
    assert created_company["name"] == company_data["name"]
    assert created_company["domain"] == company_data["domain"]
    r = client.delete(
        f"{settings.API_V1_STR}/company/delete_by_id/{created_company['id']}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert r.json() == {"msg": "Company deleted"}
    r = client.get(
        f"{settings.API_V1_STR}/company/get_by_id/{created_company['id']}",
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Company not found"


def test_delete_company_not_found(
    client: TestClient,
    superuser_token_headers: dict,
):
    r = client.delete(
        f"{settings.API_V1_STR}/company/delete_by_id/60f6e4b1c2b1f7d2c7e3f6c1",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Not found"
