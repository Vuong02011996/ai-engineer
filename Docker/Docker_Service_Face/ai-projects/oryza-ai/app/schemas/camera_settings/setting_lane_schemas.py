from typing import Optional
from app.schemas.camera_settings import SettingAIServiceBase


class SettingLaneBase(SettingAIServiceBase):
    lanes: Optional[str] = None
    """
    Lane is like this, quite complicated, so use string to store it
    "lanes": "[
    [[0.399, 0.421], [0.496, 0.73]],
    [[0.399, 0.421], [0.496, 0.73]],
    ]
    """
    key_ai: Optional[str] = None


class SettingLaneCreate(SettingLaneBase):
    lanes: str
    key_ai: str
    camera_id: str
    image_url: str
    codes: Optional[str] = None
    company_id: Optional[str] = None


class SettingLaneUpdate(SettingLaneBase):
    codes: Optional[str] = None
