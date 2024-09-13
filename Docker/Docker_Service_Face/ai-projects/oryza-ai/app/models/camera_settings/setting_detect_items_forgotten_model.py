from odmantic import Field, Model, Reference
from datetime import datetime

from app.models.camera_model import Camera
from app.common.utils.utils import datetime_now_sec


class SettingDetectItemsForgotten(Model):
    boundary: str
    waiting_time: int
    camera: Camera = Reference()
    image_url: str
    id_company: str
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
