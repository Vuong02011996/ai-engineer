from typing import Optional

from app.common.constants.enums import TypeServiceEnum
from app.schemas.base_schemas import BaseSchema
from pydantic import field_validator
from odmantic import ObjectId
from datetime import datetime
from app.models.server_model import Server
from app.models.type_service_model import TypeService


# shared properties
class ServiceBase(BaseSchema):
    name: Optional[str] = None
    port: Optional[str] = None
    is_alive: Optional[bool] = False
    max_process: Optional[int] = None
    type_service_id: Optional[str] = None
    server_id: Optional[str] = None
    type: Optional[TypeServiceEnum] = None


class ServiceCreate(ServiceBase):
    name: str
    port: str
    max_process: int
    type_service_id: str
    server_id: str
    type: TypeServiceEnum = TypeServiceEnum.ai_service


class ServiceUpdate(ServiceBase):
    pass

    @field_validator("max_process", mode="before")
    def convert_empty_max_process_to_none(cls, v):
        return None if v == "" else v

    @field_validator("is_alive", mode="before")
    def convert_empty_status_to_none(cls, v):
        return None if v == "" else v


class ServiceInDBBase(BaseSchema):
    id: ObjectId
    name: str
    port: str
    is_alive: bool
    max_process: int
    type_service: TypeService
    server: Server
    type: TypeServiceEnum


class ServiceInDB(ServiceInDBBase):
    pass


class ServiceOut(ServiceInDBBase):
    created: datetime
    modified: datetime
    server: str
    type_service: str
    count_process: Optional[int] = None

    @field_validator("server", mode="before")
    def convert_server_to_id(cls, v):
        return str(v.id) if v else None

    @field_validator("type_service", mode="before")
    def convert_type_service_to_id(cls, v):
        return str(v.id) if v else None


class ListServiceOut(BaseSchema):
    data: list[ServiceOut]
