from typing import Optional
from app.schemas.base_schemas import BaseSchema


class SettingAIServiceBase(BaseSchema):
    camera_id: Optional[str] = None
    image_url: Optional[str] = None
