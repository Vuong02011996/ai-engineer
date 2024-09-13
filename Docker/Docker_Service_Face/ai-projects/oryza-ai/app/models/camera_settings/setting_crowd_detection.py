from app.models import Camera
from app.common.utils.utils import datetime_now_sec
from odmantic import Field, Model, Reference
from datetime import datetime


class SettingCrowdDetection(Model):
    boundary: str
    min_human_count: int
    min_neighbours: int
    waiting_time_to_start_alarm: int
    waiting_time_for_next_alarm: int
    distance_threshold: int
    camera: Camera = Reference()
    image_url: str
    id_company: str
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
