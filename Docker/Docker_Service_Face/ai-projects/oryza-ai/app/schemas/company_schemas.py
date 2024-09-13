from app.schemas.base_schemas import BaseSchema
from typing import Optional
from odmantic import ObjectId
from datetime import datetime


class CompanyBase(BaseSchema):
    name: Optional[str] = None
    domain: Optional[str] = None


class CompanyCreate(BaseSchema):
    name: str
    domain: str


class CompanyUpdate(CompanyBase):
    pass


class CompanyInDBBase(CompanyBase):
    id: ObjectId


class CompanyInDB(CompanyInDBBase):
    pass


class CompanyOut(CompanyInDBBase):
    created: datetime
    modified: datetime


class ListCompanyOut(BaseSchema):
    data: list[CompanyOut]
