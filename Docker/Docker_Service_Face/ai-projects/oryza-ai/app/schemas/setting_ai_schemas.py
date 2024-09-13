from typing import Optional
from app.schemas.base_schemas import BaseSchema
from app.common.constants.enums import SettingPlateNumberEnum


class SettingBase(BaseSchema):
    camera_id: Optional[str] = None
    image_url: Optional[str] = None
    company_id: Optional[str] = None
    key_ai: Optional[str] = None


class SettingCreateBase(SettingBase):
    camera_id: str
    image_url: str


class SettingUpdateBase(SettingBase):
    image_url: Optional[str] = None


# Leaving
class SettingLeavingBase(SettingBase):
    area_str: Optional[str] = None
    object_str: Optional[str] = None
    alert_interval: Optional[int] = None
    alert_delay: Optional[int] = None


class SettingLeavingCreate(SettingCreateBase):
    area_str: str
    object_str: str
    alert_interval: int
    alert_delay: int


class SettingLeavingUpdate(SettingUpdateBase):
    area_str: Optional[str] = None
    object_str: Optional[str] = None
    alert_interval: Optional[int] = None
    alert_delay: Optional[int] = None


# Loitering (loitering and intrusion)
class SettingLoiteringCreate(SettingCreateBase):
    boundary: str
    waiting_time: int


class SettingLoiteringUpdate(SettingUpdateBase):
    boundary: Optional[str] = None
    waiting_time: Optional[int] = 0


# Tripwire
class SettingTripwireCreate(SettingCreateBase):
    line: str


class SettingTripwireUpdate(SettingUpdateBase):
    line: Optional[str] = None


# Crowd
class SettingCrowdCreate(SettingCreateBase):
    boundary: str
    min_human_count: int
    min_neighbours: int
    waiting_time_to_start_alarm: int
    waiting_time_for_next_alarm: int
    distance_threshold: int


class SettingCrowdUpdate(SettingUpdateBase):
    boundary: Optional[str] = None
    min_human_count: Optional[int] = None
    min_neighbours: Optional[int] = None
    waiting_time_to_start_alarm: Optional[int] = None
    waiting_time_for_next_alarm: Optional[int] = None
    distance_threshold: Optional[int] = None


# Lane Violation
class SettingLaneViolationCreate(SettingCreateBase):
    lanes: str
    key_ai: str
    codes: Optional[str] = None


class SettingLaneViolationUpdate(SettingUpdateBase):
    codes: Optional[str] = None


# Plate Number
class SettingPlateNumberCreate(SettingCreateBase):
    line: str
    object_detect: SettingPlateNumberEnum


class SettingPlateNumberUpdate(SettingUpdateBase):
    line: Optional[str] = None
    object_detect: Optional[SettingPlateNumberEnum] = None


# Illegal Parking
class SettingIllegalParkingCreate(SettingCreateBase):
    boundary: str
    waiting_time: int
    alert_interval: int


class SettingIllegalParkingUpdate(SettingUpdateBase):
    boundary: Optional[str] = None
    waiting_time: Optional[int] = None
    alert_interval: Optional[int] = None


class SettingObjAttrCreate(SettingCreateBase):
    line: str


class SettingObjAttrUpdate(SettingUpdateBase):
    line: Optional[str] = None
