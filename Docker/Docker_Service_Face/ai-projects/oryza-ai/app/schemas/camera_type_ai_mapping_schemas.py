from typing import Optional
from pydantic import BaseModel
from app.models.camera_model import Camera
from app.models.type_service_model import TypeService


class CameraTypeAIMappingCreateBase(BaseModel):
    camera: Optional[Camera]
    type_service: Optional[TypeService]


class CameraTypeAIMappingCreate(CameraTypeAIMappingCreateBase):
    camera: Camera
    type_service: TypeService


class CameraTypeAIMappingUpdate(CameraTypeAIMappingCreateBase):
    pass
