from typing import Dict, Any
from odmantic import Model

from app.common.enum import TypeCameraEnum


class PersonCamera(Model):
    person_id: str
    camera_id: str
    person_id_camera: str
    other_info: Dict[str, Any]
    image_id: str
    type_camera: TypeCameraEnum
