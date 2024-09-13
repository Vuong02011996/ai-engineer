from app.models import Camera
from app.common.utils.utils import datetime_now_sec
from odmantic import Field, Model, Reference
from datetime import datetime


class SettingCameraTrafficDetection(Model):
    light_boundary: str
    camera: Camera = Reference()
    image_url: str
    id_company: str
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
