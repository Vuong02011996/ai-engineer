from typing import Optional
from datetime import datetime
from odmantic import ObjectId
from pydantic import BaseModel

from app.schemas.base_schemas import BaseSchema
from app.models.camera_model import Camera




class SettingDetectItemsForgottenBase(BaseSchema):
    boundary: Optional[str] = None
    waiting_time: Optional[int] = None
    camera_id: Optional[str] = None
    image_url: Optional[str] = None
    id_company: Optional[str] = None


class SettingDetectItemsForgottenCreate(SettingDetectItemsForgottenBase):
    boundary: str
    waiting_time: int
    camera_id: str
    image_url: str


class SettingDetectItemsForgottenUpdate(BaseModel):
    boundary: Optional[str] = None
    waiting_time: Optional[int] = None
    camera_id: Optional[str] = None
    image_url: Optional[str] = None
