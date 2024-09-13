from typing import Dict

from fastapi.testclient import TestClient
from motor.core import AgnosticDatabase

from app.core.config import settings
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.services import user_services


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(
    *, client: TestClient, email: str, db: AgnosticDatabase
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = 1
    user: User = user_services.get_by_email(email=email)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        user = user_services.create_user(obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = user_services.update_user(id=user.id, obj_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
