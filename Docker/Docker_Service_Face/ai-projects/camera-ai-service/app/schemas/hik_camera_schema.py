from pydantic import BaseModel, field_validator
from typing import Optional


class Person(BaseModel):
    name: str
    sex: Optional[str] = None
    person_id: Optional[str] = None


class FaceInput(BaseModel):
    name: str
    person_id: Optional[str] = None
    sex: Optional[str] = None
    image: bytes


class HikFaceCreate(BaseModel):
    name: str
    person_id: Optional[str] = None
    image_url: str
    username: str
    password: str
    ip_address: str
    port: Optional[int] = None
    process_id: str


class Camera(BaseModel):
    username: str
    password: str
    ip_address: str
    port: Optional[int] = None

    @field_validator("port")
    def convert_port(cls, v):
        if v == 0:
            return None
        return v
