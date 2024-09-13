from app.models import Camera
from odmantic import Model, Reference, Field
from datetime import datetime
from typing import Optional

from app.common.utils.utils import datetime_now_sec
from app.common.constants.enums import SettingPlateNumberEnum


class SettingModelBase(Model):
    company_id: str

    camera: Camera = Reference()
    image_url: str
    company_id: str
    key_ai: Optional[str] = None
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)


class SettingLeavingModel(Model):
    area_str: str
    object_str: str
    alert_delay: int
    alert_interval: int

    camera: Camera = Reference()
    image_url: str
    company_id: str
    key_ai: Optional[str] = None
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)


class SettingLoiteringModel(Model):
    # for loitering and intrusion (loitering with waiting time = 0)
    boundary: str
    waiting_time: Optional[int] = 0
    key_ai: Optional[str] = None

    camera: Camera = Reference()
    image_url: str
    company_id: str
    key_ai: Optional[str] = None
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)


class SettingTripwireModel(Model):
    line: str

    camera: Camera = Reference()
    image_url: str
    company_id: str
    key_ai: Optional[str] = None
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)


class SettingCrowdModel(Model):
    boundary: str
    min_human_count: int
    min_neighbours: int
    waiting_time_to_start_alarm: int
    waiting_time_for_next_alarm: int
    distance_threshold: int

    camera: Camera = Reference()
    image_url: str
    company_id: str
    key_ai: Optional[str] = None
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)


class SettingLaneViolationModel(Model):
    lanes: str

    camera: Camera = Reference()
    key_ai: str
    image_url: str
    company_id: str
    codes: Optional[str] = None
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)


class SettingPlateNumberModel(Model):
    line: str
    object_detect: SettingPlateNumberEnum

    camera: Camera = Reference()
    image_url: str
    company_id: str
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)


class SettingIllegalParkingModel(Model):
    boundary: str
    waiting_time: int
    alert_interval: int

    camera: Camera = Reference()
    image_url: str
    company_id: str
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)


class SettingObjAttrModel(Model):
    line: str

    camera: Camera = Reference()
    image_url: str
    company_id: str
    key_ai: Optional[str] = None
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
