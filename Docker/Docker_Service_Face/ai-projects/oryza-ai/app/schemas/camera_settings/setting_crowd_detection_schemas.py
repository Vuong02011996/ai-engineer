from typing import Optional

from pydantic import BaseModel

from app.schemas.base_schemas import BaseSchema


class SettingCrowdDetectionBase(BaseSchema):
    boundary: Optional[str] = None
    min_human_count: Optional[int] = None
    min_neighbours: Optional[int] = None
    distance_threshold: Optional[int] = None
    waiting_time_to_start_alarm: Optional[int] = None
    waiting_time_for_next_alarm: Optional[int] = None
    camera_id: Optional[str] = None
    image_url: Optional[str] = None
    id_company: Optional[str] = None


class SettingCrowdDetectionCreate(SettingCrowdDetectionBase):
    boundary: str
    min_human_count: int
    min_neighbours: int
    waiting_time_to_start_alarm: int
    waiting_time_for_next_alarm: int
    distance_threshold: int
    camera_id: str
    image_url: str


class SettingCrowdDetectionUpdate(BaseModel):
    boundary: Optional[str] = None
    min_human_count: Optional[int] = None
    min_neighbours: Optional[int] = None
    distance_threshold: Optional[int] = None
    waiting_time_to_start_alarm: Optional[int] = None
    waiting_time_for_next_alarm: Optional[int] = None
    image_url: Optional[str] = None
