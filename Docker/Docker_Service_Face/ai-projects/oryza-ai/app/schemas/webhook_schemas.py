from typing import Optional
from odmantic import ObjectId
from datetime import datetime
from pydantic import field_validator

from app.schemas.base_schemas import BaseSchema
from app.models.company_model import Company
from app.models.type_service_model import TypeService


class WebhookCreate(BaseSchema):
    name: str
    endpoint: str
    status: Optional[bool] = False
    type_service_id: Optional[str] = None
    token: str
    auth_type: str


class WebhookUpdate(BaseSchema):
    name: Optional[str] = None
    endpoint: Optional[str] = None
    status: Optional[bool] = None
    type_service_id: Optional[str] = None
    token: Optional[str] = None
    auth_type: Optional[str] = None


class WebhookInDBBase(BaseSchema):
    id: ObjectId
    company: Company
    type_service: Optional[TypeService]
    status: bool
    name: str
    endpoint: str
    token: str
    auth_type: str


class WebhookInDB(WebhookInDBBase):
    pass


class WebhookOut(WebhookInDBBase):
    created: datetime
    modified: datetime
    company: str
    type_service: dict

    @field_validator("company", mode="before")
    def convert_company_to_id(cls, v):
        return str(v.id) if v else None

    @field_validator("type_service", mode="before")
    def convert_type_service_to_id(cls, v):
        return {"id": str(v.id), "name": v.name} if v else None


class ListWebhookOut(BaseSchema):
    data: list[WebhookOut]
