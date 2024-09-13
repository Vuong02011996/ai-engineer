from fastapi.testclient import TestClient
from faker import Faker

from app.schemas.user_schemas import UserCreate, UserUpdateMe
from app.core.config import settings
from app.services import user_services
from app.tests.init_db import init_data as data

fake = Faker()


# CREATE
def test_create_user_superuser(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    """Test create user with superuser token."""
    company1 = data["company"][0]
    fake = Faker()
    new_user = UserCreate(
        email=fake.email(),
        username=fake.user_name(),
        password="password",
        company_id=company1["id"],
        is_superuser=False,
        is_active=True,
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/user/create",
        headers=superuser_token_headers,
        json=new_user,
    )
    user_created = r.json()
    assert user_created["email"] == new_user["email"]
    assert user_created["username"] == new_user["username"]
    assert not user_created["is_superuser"]
    assert user_created["is_active"]
    # Delete the user
    try:
        user_services.remove(id=user_created["id"])
    except Exception:
        assert False


def test_create_user_no_permission(client: TestClient) -> None:
    """Test create user with no token."""
    company1 = data["company"][0]
    fake = Faker()
    new_user = UserCreate(
        email=fake.email(),
        username=fake.user_name(),
        password="1",
        company_id=company1["id"],
        is_superuser=False,
        is_active=False,
    ).model_dump()
    r = client.post(f"{settings.API_V1_STR}/user/register", json=new_user)
    assert r.status_code == 201
    user = r.json()
    assert user["email"] == new_user["email"]
    assert user["username"] == new_user["username"]
    assert not user["is_superuser"]
    assert not user["is_active"]
    # Delete the user
    user_services.remove(id=user["id"])


def test_create_user_duplicate_email(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    """Test create user with duplicate email."""
    company1 = data["company"][0]
    new_user = UserCreate(
        email=settings.FIRST_USER_EMAIL,
        username=fake.user_name(),
        password="1",
        company_id=company1["id"],
        is_superuser=False,
        is_active=True,
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/user/create",
        headers=superuser_token_headers,
        json=new_user,
    )
    assert r.status_code == 400
    assert r.json() == {"detail": "Email already used"}


def test_create_user_duplicate(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    """Test create user with duplicate username."""
    company1 = data["company"][0]
    new_user = UserCreate(
        email=settings.FIRST_USER_EMAIL,
        username=settings.FIRST_USER_USERNAME,
        password="1",
        company_id=company1["id"],
        is_superuser=False,
        is_active=True,
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/user/create",
        headers=superuser_token_headers,
        json=new_user,
    )
    assert r.status_code == 400
    assert r.json() == {"detail": "Username already used"} or r.json() == {
        "detail": "Email already used"
    }


def test_register_user_duplicate(
    client: TestClient,
):
    """Test create user with duplicate username."""
    company1 = data["company"][0]
    new_user = UserCreate(
        email=settings.FIRST_USER_EMAIL,
        username=settings.FIRST_USER_USERNAME,
        password="1",
        company_id=company1["id"],
        is_superuser=False,
        is_active=True,
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/user/register",
        json=new_user,
    )
    assert r.status_code == 400
    assert r.json() == {"detail": "Username already used"} or r.json() == {
        "detail": "Email already used"
    }


# GET
def test_count_user(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    """Test count users with superuser token."""
    r = client.get(f"{settings.API_V1_STR}/user/count", headers=superuser_token_headers)
    count = r.json()
    assert count
    assert count["count"] > 0


def test_count_user_no_permission(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Test count users with normal user token."""
    r = client.get(
        f"{settings.API_V1_STR}/user/count", headers=normal_user_token_headers
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "Not enough permissions"}


def test_get_user_me_superuser(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    """Test get current user with superuser token."""
    r = client.get(
        f"{settings.API_V1_STR}/user/get/me", headers=superuser_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER_EMAIL


def test_get_user_me_nomal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Test get current user with normal user token."""
    r = client.get(
        f"{settings.API_V1_STR}/user/get/me", headers=normal_user_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert not current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_USER_EMAIL


def test_get_all_users(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    """Test get all users with superuser token."""
    r = client.get(
        f"{settings.API_V1_STR}/user/get_all", headers=superuser_token_headers
    )
    users = r.json()
    assert users
    users = users["data"]
    for user in users:
        assert "email" in user
        assert "is_active" in user
        assert "is_superuser" in user


def test_get_all_user_no_permission(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Test get all users with normal user token."""
    r = client.get(
        f"{settings.API_V1_STR}/user/get_all", headers=normal_user_token_headers
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "Not enough permissions"}


def test_get_user_by_id(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    """Test get user by id with superuser token."""

    normal_user = data["normal_user"][0]
    r = client.get(
        f"{settings.API_V1_STR}/user/get_by_id/{normal_user['id']}",
        headers=superuser_token_headers,
    )
    created_user = r.json()
    assert created_user
    assert created_user["email"] == normal_user["email"]
    assert created_user["is_active"] == normal_user["is_active"]
    assert created_user["is_superuser"] == normal_user["is_superuser"]
    assert created_user["id"] == normal_user["id"]
    assert created_user["company"] == normal_user["company"]
    assert created_user["username"] == normal_user["username"]


def test_get_user_by_id_no_permission(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    superuser = data["superuser"]
    superuser_id = superuser["id"]
    r = client.get(
        f"{settings.API_V1_STR}/user/get_by_id/{superuser_id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "Not enough permissions"}


def test_get_user_by_id_wrong(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/user/get_by_id/123", headers=superuser_token_headers
    )
    assert r.status_code == 400
    assert r.json() == {"detail": "Invalid ID"}


def test_retrieve_user_by_id_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/user/get_by_id/614a5f5b8d7c8d6d1b4f7d8b",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json() == {"detail": "User not found"}


# UPDATE
def test_update_me(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    fake = Faker()
    fake_name = fake.name()
    fake_username = fake.user_name()
    user_update = UserUpdateMe(full_name=fake_name, username=fake_username).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/user/update/me",
        headers=normal_user_token_headers,
        json=user_update,
    )
    assert r.status_code == 200
    user = r.json()
    assert user["full_name"] == fake_name
    assert user["username"] == fake_username
    # Reset the user
    user_update = UserUpdateMe(
        full_name="", username=settings.FIRST_USER_USERNAME
    ).model_dump()
    user_services.update_user(obj_in=user_update, id=user["id"])


def test_update_me_duplicate_username(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    user_update = UserUpdateMe(username=settings.FIRST_SUPERUSER_USERNAME).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/user/update/me",
        headers=normal_user_token_headers,
        json=user_update,
    )
    assert r.status_code == 400
    assert r.json() == {"detail": "Username already used"}


def test_update_me_wrong_password(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    user_update = UserUpdateMe(current_password="2", new_password="1").model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/user/update/me",
        headers=normal_user_token_headers,
        json=user_update,
    )
    assert r.status_code == 400
    assert r.json() == {"detail": "Wrong username or password"}


def test_update_user_by_id_superuser(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    normal_user = data["normal_user"][0]
    fake = Faker()
    fake_name = fake.name()
    fake_username = fake.user_name()
    user_update = UserUpdateMe(full_name=fake_name, username=fake_username).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/user/update_by_id/{normal_user['id']}",
        headers=superuser_token_headers,
        json=user_update,
    )
    assert r.status_code == 200
    user = r.json()
    assert user["full_name"] == fake_name
    assert user["username"] == fake_username
    # Reset the user
    user_update = UserUpdateMe(
        full_name="", username=settings.FIRST_USER_USERNAME
    ).model_dump()
    user_services.update_user(obj_in=user_update, id=user["id"])


def test_update_user_by_id_by_himself(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    normal_user = data["normal_user"][0]
    fake = Faker()
    fake_name = fake.name()
    fake_username = fake.user_name()
    user_update = UserUpdateMe(full_name=fake_name, username=fake_username).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/user/update_by_id/{normal_user['id']}",
        headers=normal_user_token_headers,
        json=user_update,
    )
    assert r.status_code == 200
    user = r.json()
    assert user["full_name"] == fake_name
    assert user["username"] == fake_username
    # Reset the user
    user_update = UserUpdateMe(
        full_name="", username=settings.FIRST_USER_USERNAME
    ).model_dump()
    user_services.update_user(obj_in=user_update, id=user["id"])


def test_update_user_by_id_no_permission(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    superuser = data["superuser"]
    user_update = UserUpdateMe(full_name="test", username="test").model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/user/update_by_id/{superuser['id']}",
        headers=normal_user_token_headers,
        json=user_update,
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "Not enough permissions"}


def test_update_user_by_id_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    user_update = UserUpdateMe(full_name="test", username="test").model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/user/update_by_id/{data['fake_id']}",
        headers=superuser_token_headers,
        json=user_update,
    )
    assert r.status_code == 404
    assert r.json() == {"detail": "User not found"}


def test_update_user_by_id_duplicate_username(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    normal_user = data["normal_user"][0]
    user_update = UserUpdateMe(username=settings.FIRST_SUPERUSER_USERNAME).model_dump()
    r = client.put(
        f"{settings.API_V1_STR}/user/update_by_id/{normal_user['id']}",
        headers=superuser_token_headers,
        json=user_update,
    )
    assert r.status_code == 400
    assert r.json() == {"detail": "Username already used"}


# DELETE
def test_delete_user(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    company1 = data["company"][0]
    fake = Faker()
    new_user = UserCreate(
        email=fake.email(),
        username=fake.user_name(),
        password="password",
        company_id=company1["id"],
        is_superuser=False,
        is_active=True,
    ).model_dump()
    r = client.post(
        f"{settings.API_V1_STR}/user/create",
        headers=superuser_token_headers,
        json=new_user,
    )
    new_user = r.json()
    r = client.delete(
        f"{settings.API_V1_STR}/user/delete_by_id/{new_user['id']}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert r.json() == {"msg": "User deleted"}


def test_delete_user_no_permission(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    superuser = data["superuser"]
    r = client.delete(
        f"{settings.API_V1_STR}/user/delete_by_id/{superuser['id']}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "Not enough permissions"}


def test_delete_user_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/user/delete_by_id/{data['fake_id']}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json() == {"detail": "Not found"}
