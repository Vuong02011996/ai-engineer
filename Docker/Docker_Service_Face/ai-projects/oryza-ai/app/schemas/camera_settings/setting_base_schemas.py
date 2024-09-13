from typing import Optional

from pydantic import BaseModel

from app.schemas.base_schemas import BaseSchema


class SettingBase(BaseSchema):
    camera_id: Optional[str] = None
    image_url: Optional[str] = None
    id_company: Optional[str] = None


class SettingCreateBase(SettingBase):
    camera_id: str
    image_url: str


class SettingUpdateBase(BaseModel):
    image_url: Optional[str] = None
