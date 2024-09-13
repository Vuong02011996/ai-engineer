from app.schemas.base_schemas import BaseSchema
from typing import Optional
from odmantic import ObjectId
from datetime import datetime


class VMSBase(BaseSchema):
    ip_address: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    vms_type: Optional[str] = None


class VMSCreate(BaseSchema):
    ip_address: str
    port: Optional[int]
    username: str
    password: str
    vms_type: str


class VMSCreateInDB(VMSCreate):
    company_id: str


class VMSUpdate(VMSBase):
    pass


class VMSOut(VMSBase):
    id: ObjectId
    created: datetime
    modified: datetime


class ListVMSOut(BaseSchema):
    data: list[VMSOut]


class LoginInfo(BaseSchema):
    username: str
    password: str
    port: int
    ip_address: str
    vms_type: str
