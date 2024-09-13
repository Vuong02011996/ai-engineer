from enum import Enum


class RequestType(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


# class ProcessType(str, Enum):
#     ai_camera = "AI_CAMERA"
#     ai_service = "AI_SERVICE"


class ProcessStatus(str, Enum):
    start = "START"
    stop = "STOP"
    pause = "PAUSE"


class TypeServiceEnum(str, Enum):
    ai_camera = "AI_CAMERA"
    ai_service = "AI_SERVICE"


class AuthType(str, Enum):
    header = "header"


class SettingPlateNumberEnum(str, Enum):
    PLATE = "plate"
    VEHICLE = "vehicle"


class RoleEnum(str, Enum):
    admin = "ADMIN"
    user = "USER"
    superuser = "SUPERUSER"


class VmsTypeEnum(str, Enum):
    nx = "nx"
    oryza = "oz"


# for 3rd
class GeoUnitType(str, Enum):
    province = "province"
    district = "district"
    ward = "ward"
