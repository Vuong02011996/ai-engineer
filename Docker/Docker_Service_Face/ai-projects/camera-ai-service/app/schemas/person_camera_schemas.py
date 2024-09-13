from typing import Optional
from odmantic import ObjectId
from pydantic import BaseModel

from app.common.enum import TypeCameraEnum


class PersonCameraBase(BaseModel):
    person_id: Optional[str] = None
    camera_id: Optional[str] = None
    person_id_camera: Optional[str] = None
    other_info: Optional[dict] = None
    image_id: Optional[str] = None
    type_camera: Optional[TypeCameraEnum] = None


class PersonCameraCreate(PersonCameraBase):
    person_id: str
    camera_id: str
    person_id_camera: str
    image_id: str
    type_camera: TypeCameraEnum


class Camera(BaseModel):
    id: str
    key: str


class PersonCameraCreateDTO(BaseModel):
    person_id: str
    id_camera: str
    key_camera: str
    host_camera: str
    username_camera: str
    password_camera: str
    port_camera: str


class CameraBase(BaseModel):
    key_camera: str
    host_camera: str
    username_camera: str
    password_camera: str
    port_camera: str


class PersonCameraDelete(CameraBase):
    pass


class PersonCameraCreateMultiCameraUser(CameraBase):
    id_camera: str


class PersonCameraUpdate(PersonCameraBase):
    pass


class PersonCameraInDBBase(PersonCameraBase):
    id: ObjectId


class PersonCameraInDB(PersonCameraInDBBase):
    pass


class PersonCameraOut(PersonCameraInDBBase):
    pass


class ListPersonCamera(BaseModel):
    data: list[PersonCameraOut]
