from pydantic import BaseModel
from typing import Optional


class CameraHik(BaseModel):
    address: str
    port: str
    username: str
    password: str


class GetPersonCameraHik(CameraHik):
    pid: str


class CreatePersonCameraHik(CameraHik):
    name: str
    custom_pid: Optional[str] = None
    image: bytes


class DeletePersonCameraHik(CameraHik):
    pid: str


class UpdateImagePersonCameraHik(CameraHik):
    pid: str
    image: bytes


class UpdateInfoPersonCameraHik(CameraHik):
    pid: str
    name: str
