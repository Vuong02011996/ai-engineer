from fastapi import APIRouter, HTTPException, Request
from typing import Any
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm

from app.core import security
from app.core.config import settings
from app.schemas.user_schemas import UserLogin
from app.models.token_models import Token
from app.services.user_services import user_services

router = APIRouter()


# OAuth2 compatible token for login
@router.post("/access-token", response_model=Token, status_code=201)
async def login_access_token(
    request: Request,
) -> Any:
    content_type = request.headers.get("content-type")
    if content_type == "application/x-www-form-urlencoded":
        form_data = await request.form()
        login = OAuth2PasswordRequestForm(**form_data)
    elif content_type == "application/json":
        request_json = await request.json()
        if not request_json:
            raise HTTPException(status_code=400, detail="Invalid json")
        if "username" not in request_json or "password" not in request_json:
            raise HTTPException(status_code=400, detail="Invalid json")
        login = UserLogin(**await request.json())
    else:
        raise HTTPException(status_code=400, detail="Invalid content type")

    user = user_services.authenticate(email=login.username, password=login.password)
    if not login.password or not user:
        raise HTTPException(
            status_code=400, detail="Login failed; incorrect email or password"
        )
    if not user_services.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # lấy ngày hết hạn của token
    expire = (datetime.now().timestamp() + access_token_expires.total_seconds()) * 1000
    # convert expire thành miliseconds
    # expire = expire.timestamp() * 1000
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "expire": int(expire),
    }
