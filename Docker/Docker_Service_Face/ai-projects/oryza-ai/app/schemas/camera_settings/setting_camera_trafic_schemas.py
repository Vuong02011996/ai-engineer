from typing import Optional

from pydantic import BaseModel

from app.schemas.base_schemas import BaseSchema


class SettingCameraTrafficBase(BaseSchema):
    light_boundary: Optional[str] = None
    camera_id: Optional[str] = None
    image_url: Optional[str] = None
    id_company: Optional[str] = None


class SettingCameraTrafficCreate(SettingCameraTrafficBase):
    light_boundary: str
    camera_id: str
    image_url: str


class SettingCameraTrafficUpdate(BaseModel):
    light_boundary: Optional[str] = None
    image_url: Optional[str] = None
