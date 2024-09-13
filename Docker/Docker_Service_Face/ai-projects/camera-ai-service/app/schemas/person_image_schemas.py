from typing import Optional
from odmantic import ObjectId
from pydantic import BaseModel


class PersonImageBase(BaseModel):
    name: Optional[str] = None
    person_id: Optional[str] = None
    url: Optional[str] = None
    # array of ImageEnum
    # type: Optional[list[ImageEnum]] = []


class PersonImageCreate(PersonImageBase):
    name: str
    person_id: str
    url: str


class PersonImageUpdateAuto(BaseModel):
    id_person: str
    key_camera: str
    host_camera: str
    username_camera: str
    password_camera: str
    port_camera: str
    id_person_camera: str


class PersonImageUpdate(PersonImageBase):
    pass


class PersonImageInDBBase(PersonImageBase):
    id: ObjectId


class PersonImageInDB(PersonImageInDBBase):
    pass


class PersonOut(PersonImageInDBBase):
    pass


class ListPerson(BaseModel):
    data: list[PersonOut]
