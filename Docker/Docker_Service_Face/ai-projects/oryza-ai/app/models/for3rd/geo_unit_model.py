from datetime import datetime
from odmantic import Field, Model
from typing import Optional
from app.common.constants.enums import GeoUnitType
from app.common.utils.utils import datetime_now_sec


class GeoUnit(Model):
    name: str
    province_id: Optional[str] = None
    district_id: Optional[str] = None
    ward_id: Optional[str] = Field(default=None)
    type: Optional[GeoUnitType] = None
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
