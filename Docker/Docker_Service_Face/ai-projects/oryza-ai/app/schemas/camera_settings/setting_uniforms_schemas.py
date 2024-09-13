from typing import Optional

from pydantic import BaseModel

from app.schemas.base_schemas import BaseSchema


class SettingUniformsBase(BaseSchema):
    boundary: Optional[str] = None
    waiting_time: Optional[int] = None
    # rgb: Optional[str] = None
    camera_id: Optional[str] = None
    image_url: Optional[str] = None
    id_company: Optional[str] = None


class SettingUniformsCreate(SettingUniformsBase):
    boundary: str
    waiting_time: int
    # rgb: str
    camera_id: str
    image_url: str


class SettingUniformsUpdate(BaseModel):
    boundary: Optional[str] = None
    waiting_time: Optional[int] = None
    # rgb: Optional[str] = None
    image_url: Optional[str] = None
