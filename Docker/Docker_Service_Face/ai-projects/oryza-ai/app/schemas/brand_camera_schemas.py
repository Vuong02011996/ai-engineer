from app.schemas.base_schemas import BaseSchema

from typing import Optional
from datetime import datetime
from odmantic import ObjectId


class BrandCameraCreate(BaseSchema):
    name: str
    key: str


class BrandCameraUpdate(BaseSchema):
    name: Optional[str] = None
    key: Optional[str] = None


class BrandCameraOut(BaseSchema):
    id: ObjectId
    name: str
    key: str
    created: datetime
    modified: datetime


class ListBrandCameraOut(BaseSchema):
    data: list[BrandCameraOut]
