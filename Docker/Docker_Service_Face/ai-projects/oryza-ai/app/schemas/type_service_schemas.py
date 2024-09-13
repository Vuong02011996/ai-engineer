from typing import Optional
from app.schemas.base_schemas import BaseSchema
from datetime import datetime
from odmantic import ObjectId


# shared properties
class TypeServiceBase(BaseSchema):
    name: Optional[str] = None
    key: Optional[str] = None


class TypeServiceCreate(TypeServiceBase):
    name: str
    key: str


class TypeServiceUpdate(TypeServiceBase):
    pass


class TypeServiceInDBBase(TypeServiceBase):
    id: ObjectId


class TypeServiceInDB(TypeServiceInDBBase):
    pass


class TypeServiceOut(TypeServiceInDBBase):
    created: datetime
    modified: datetime


class ListTypeServiceOut(BaseSchema):
    data: list[TypeServiceOut]
