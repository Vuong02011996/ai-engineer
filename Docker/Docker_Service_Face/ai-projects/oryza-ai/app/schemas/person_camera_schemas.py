from pydantic import BaseModel

from app.common.constants.type_camera import TypeCameraEnum


class PersonCameraCreate(BaseModel):
    person_id: str
    # id_camera or id_service
    id_camera: str
    key_camera: TypeCameraEnum

class PersonCameraDelete(BaseModel):
    key_camera: str
    id_camera: str
