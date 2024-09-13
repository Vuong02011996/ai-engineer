from typing import Any

from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.webhook_schemas import (
    WebhookOut,
    WebhookCreate,
    WebhookUpdate,
)
from app.schemas.base_schemas import Msg, Count
from app.models.user_model import User

# from app.services import webhook_services
from app.services.webhook_services import webhook_services
from app.common.constants.enums import AuthType

router = APIRouter()


@router.post("/create", response_model=WebhookOut, status_code=201)
def create_webhook(
    request: WebhookCreate,
    current_user: User = Depends(deps.get_current_active_admin),
) -> WebhookOut:
    return webhook_services.create_webhook(user=current_user, obj_in=request)


@router.get("/get_all", response_model=Any, status_code=200)
def get_all_webhooks(
    current_user: User = Depends(deps.get_current_active_admin),
    page: int = 0,
    page_break: bool = False,
    data_search: str = None,
) -> Any:
    return {
        "data": webhook_services.get_webhooks(
            user=current_user, page=page, page_break=page_break, data_search=data_search
        )
    }


@router.get(
    "/count",
    status_code=200,
    response_model=Count,
)
def count_webhook(
    current_user: User = Depends(deps.get_current_active_admin),
    data_search: str = None,
) -> Any:
    return Count(
        count=webhook_services.get_count(user=current_user, data_search=data_search)
    )


@router.get("/get_by_id/{webhook_id}", response_model=WebhookOut, status_code=200)
def get_webhook_by_id(
    webhook_id: str,
    current_user: User = Depends(deps.get_current_active_admin),
) -> WebhookOut:
    return webhook_services.get_webhook(user=current_user, id=webhook_id)


@router.put("/update_by_id/{webhook_id}", response_model=WebhookOut, status_code=200)
def update_webhook_by_id(
    webhook_id: str,
    request: WebhookUpdate,
    current_user: User = Depends(deps.get_current_active_admin),
) -> WebhookOut:
    return webhook_services.update_webhook(
        user=current_user, id=webhook_id, obj_in=request
    )


@router.delete(
    "/delete_by_id/{webhook_id}",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def delete_webhook_by_id(
    webhook_id: str,
) -> Msg:
    webhook_services.remove_webhook(id=webhook_id)
    return {"msg": "Webhook deleted"}


@router.get("/get_auth_type", status_code=200)
def get_auth_type():
    return {"data": [auth_type.value for auth_type in AuthType]}
