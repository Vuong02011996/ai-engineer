from odmantic import Field, Model, Reference
from datetime import datetime

from app.models.camera_model import Camera
from app.common.utils.utils import datetime_now_sec


class SettingBase(Model):
    camera: Camera = Reference()
    company_id: str
    image_url: str
    id_company: str
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)


class SettingCrowdDetection(SettingBase):
    boundary: str
    min_human_count: int
    min_neighbours: int
    waiting_time_to_start_alarm: int
    waiting_time_for_next_alarm: int
    distance_threshold: int


class SettingDetectItemsForgotten(SettingBase):
    boundary: str
    waiting_time: int


class SettingLoiteringDetection(SettingBase):
    boundary: str
    waiting_time: int


class SettingPlateDetection(SettingBase):
    boundary: str
    type_object: str
    confidence: float
