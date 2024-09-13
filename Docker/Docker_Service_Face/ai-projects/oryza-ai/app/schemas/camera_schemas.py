from typing import Optional
from odmantic import ObjectId
from pydantic import BaseModel, field_validator, Field
from datetime import datetime

from app.schemas.base_schemas import BaseSchema


class CameraBase(BaseSchema):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    rtsp: Optional[str] = None
    rtsp_vms: Optional[str] = None
    is_ai: Optional[bool] = None
    other_info: Optional[dict] = None
    vms_type: Optional[str] = None
    ward_id: Optional[str] = Field(default=None)


class CameraCreate(BaseModel):
    name: str
    ip_address: str
    port: Optional[int] = None
    username: str
    password: str
    rtsp: str
    brand_camera_id: Optional[str] = None
    is_ai: bool = False
    other_info: dict
    type_service_ids: list[str]
    vms_type: Optional[str] = None
    rtsp_vms: Optional[str] = None
    ward_id: Optional[str] = None


class CameraUpdate(CameraBase):
    brand_camera_id: Optional[str] = None
    type_service_ids: Optional[list[str]] = None


class CameraInDBBase(CameraBase):
    id: ObjectId


class CameraInDB(CameraInDBBase):
    pass


class CameraOut(CameraInDBBase):
    company: str
    brand_camera: dict
    created: datetime
    modified: datetime

    @field_validator("company", mode="before")
    def convert_company_to_str(cls, v):
        return str(v.id) if v else None

    @field_validator("brand_camera", mode="before")
    def convert_brand_camera_to_str(cls, v):
        return {"id": str(v.id), "key": v.key} if v else None


class ListCameraOut(BaseSchema):
    data: list[CameraOut]


class GenerateRTSP(BaseSchema):
    address: str
    port: int
    username: str
    password: str
