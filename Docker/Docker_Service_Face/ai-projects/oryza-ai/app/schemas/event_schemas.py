from typing import Optional, Any, Dict

from app.models.company_model import Company
from app.models.type_service_model import TypeService
from app.schemas.base_schemas import BaseSchema
from datetime import datetime
from odmantic import ObjectId
from pydantic import BaseModel, field_validator


class EventBase(BaseSchema):
    camera: Optional[str] = None
    type_service: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    company: Optional[str] = None


class EventCreate(BaseModel):
    type_service: TypeService
    data: Dict[str, Any]
    camera: str
    company: Company


class EventUpdate(EventBase):
    pass


class EventUpdateFace(BaseSchema):
    user_id: str
    name: str
    list_id_event: list[str]


class EventInDBBase(BaseSchema):
    id: ObjectId
    data: dict[str, Any]
    camera: str
    type_service: TypeService
    company: Company


# class CompanyInDB(EventInDBBase):
#     pass


class EventOut(EventInDBBase):
    type_service: str
    camera: str
    company: str
    created: datetime
    # modified: datetime

    @field_validator("company", mode="before")
    def convert_company_to_str(cls, v):
        return str(v["id"]) if v else None

    @field_validator("type_service", mode="before")
    def convert_type_service_to_str(cls, v):
        return str(v["id"]) if v else None


class ListEventOut(BaseSchema):
    data: list[EventOut]


class SearchCondition(BaseSchema):
    """Search condition for get event image by camera"""

    camera_id: str
    type_service_id: Optional[str] = None
    start_time: int
    end_time: int
