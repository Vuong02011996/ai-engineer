from app.models import Camera
from app.common.utils.utils import datetime_now_sec
from odmantic import Field, Model, Reference
from datetime import datetime
from typing import Optional


class SettingLane(Model):
    lanes: str
    camera: Camera = Reference()
    key_ai: str
    image_url: str
    company_id: str
    codes: Optional[str] = None
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
