from typing import Optional
from pydantic import BaseModel, field_validator
from odmantic import ObjectId
from datetime import datetime

from app.common.constants.enums import GeoUnitType


class GeoUnitBase(BaseModel):
    name: Optional[str] = None
    province_id: Optional[str] = None
    district_id: Optional[str] = None
    ward_id: Optional[str] = None
    type: GeoUnitType


class GeoUnitCreate(GeoUnitBase):
    pass


class GeoUnitUpdate(GeoUnitBase):
    pass


class GeoUnitGet(BaseModel):
    page: int = 0
    page_break: bool = False
    parent_id: Optional[str] = None
    type: Optional[GeoUnitType] = None
    keyword: Optional[str] = None


class GeoUnitOut(BaseModel):
    id: ObjectId
    name: str
    type: str

    @field_validator("id", mode="before")
    def convert_id_to_str(cls, v):
        return str(v) if v else None


class ListGeoUnitOut(BaseModel):
    data: list[GeoUnitOut]


class GeoUnitGetDetail(GeoUnitBase):
    id: ObjectId
    created: datetime
    modified: datetime

    @field_validator("id", mode="before")
    def convert_id_to_str(cls, v):
        return str(v) if v else None
