from typing import Optional

from pydantic import BaseModel

from app.schemas.base_schemas import BaseSchema


class SettingTamperingBase(BaseSchema):
    alarm_interval: Optional[int] = None
    # rgb: Optional[str] = None
    camera_id: Optional[str] = None
    # image_url: Optional[str] = None
    id_company: Optional[str] = None


class SettingTamperingCreate(SettingTamperingBase):
    alarm_interval: int
    # rgb: str
    camera_id: str
    # image_url: str


class SettingTamperingUpdate(BaseModel):
    alarm_interval: Optional[int] = None
    # rgb: Optional[str] = None
    # image_url: Optional[str] = None
