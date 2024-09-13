from typing import Optional
from odmantic import ObjectId
from pydantic import BaseModel

from app.schemas.person_camera_schemas import PersonCameraCreateMultiCameraUser


class PersonBase(BaseModel):
    name: Optional[str] = None
    company_id: Optional[str] = None
    other_info: Optional[dict] = None


class PersonCreate(PersonBase):
    name: str
    company_id: str


class PersonRegister(BaseModel):
    name: str
    data: list[str]
    list_camera: list[PersonCameraCreateMultiCameraUser]


class PersonModify(BaseModel):
    name: Optional[str] = None
    data: list[str]
    user_id: str


class PersonUpdate(PersonBase):
    pass


class PersonInDBBase(PersonBase):
    id: ObjectId


class PersonInDB(PersonInDBBase):
    pass


class PersonOut(PersonInDBBase):
    pass


class ListPerson(BaseModel):
    data: list[PersonOut]
