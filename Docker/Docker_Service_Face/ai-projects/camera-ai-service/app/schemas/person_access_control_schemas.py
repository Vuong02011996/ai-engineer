from pydantic import BaseModel
# from typing import Optional


class CameraBase(BaseModel):
    address: str
    port: str
    username: str
    password: str


class CreatePersonCameraAccessControl(CameraBase):
    person_name: str
    pid: str
    image: bytes


class GetPersonCameraAccessControl(BaseModel):
    pass


class UpdateImagePersonCameraAccessControl(CameraBase):
    image: bytes
    user_id: str


class DeletePersonCameraAccessControl(CameraBase):
    recno: str
