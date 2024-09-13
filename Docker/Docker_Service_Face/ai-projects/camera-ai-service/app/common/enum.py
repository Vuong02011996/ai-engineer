from enum import Enum


class VehicleTypeEnum(str, Enum):
    car = "car"
    motorcycle = "motorcycle"


class VehicleBrand(str, Enum):
    unknown = "Không xác định"


class SexEnum(str, Enum):
    Male = "Male"
    Female = "Female"
    Unknown = "Unknown"


class TypeCameraEnum(str, Enum):
    dahua = "DAHUA"
    face_service = "FACE_SERVICE"
    hikvision = "HIKVISION"
    access_control = "ACCESS_CONTROL"  # dahua
    kbvision = "KBVISION"


class TrafficIntelligentStatusEnum(str, Enum):
    yes = "yes"
    no = "no"
    na = "na"  # not available


class Color(str, Enum):
    silver = "Bạc"
    white = "Trắng"
    black = "Đen"
    red = "Đỏ"
    blue = "Xanh dương"
    green = "Xanh lục"
    yellow = "Vàng"
    orange = "Cam"
    brown = "Nâu"
    purple = "Tím"
    pink = "Hồng"
    gray = "Xám"
    darkorange = "Cam đậm"
    darkblue = "Xanh đậm"
    unknown = "Không xác định"
