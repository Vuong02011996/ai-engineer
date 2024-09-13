from enum import Enum


class TypeCameraEnum(str, Enum):
    hikvision = "HIKVISION"
    dahua = "DAHUA"
    face_service = "FACE_SERVICE"
    access_control = "ACCESS_CONTROL"
    kbvision = "KBVISION"