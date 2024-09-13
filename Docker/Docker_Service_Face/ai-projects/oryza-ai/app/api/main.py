from fastapi import APIRouter
from app.api.routes import (
    login_routes,
    setting_ai_service_base_routes,
    user_routes,
    service_routes,
    process_routes,
    camera_routes,
    company_routes,
    webhook_routes,
    type_service_routes,
    server_routes,
    event_routes,
    brand_camera_routes,
    vms_routes,
    camera_type_ai_mapping_routes,
    person_routers,
    person_camera_router,
    person_image_router,
    upload_routes,
    video_analyze_routes,
)
from app.api.routes.camera_settings import (
    setting_detect_items_forgotten_routes,
    setting_uniform_detection_routes,
    setting_uniform_config_company,
    setting_tampering_routes,
    setting_camera_traffic_detection_routes,
)
from app.api.routes.for3rd import geo_unit_routes

from app.schemas.camera_settings import SettingLaneCreate, SettingLaneUpdate
from app.services.camera_settings import st_lane_sv

from app.schemas import (
    SettingLeavingCreate,
    SettingLeavingUpdate,
    SettingTripwireCreate,
    SettingTripwireUpdate,
    SettingLoiteringCreate,
    SettingLoiteringUpdate,
    SettingPlateNumberCreate,
    SettingPlateNumberUpdate,
    SettingIllegalParkingCreate,
    SettingIllegalParkingUpdate,
    SettingCrowdCreate,
    SettingCrowdUpdate,
    SettingObjAttrCreate,
    SettingObjAttrUpdate,
)
from app.services import (
    st_leaving_sv,
    st_tripwire_sv,
    st_loitering_sv,
    st_plate_number_sv,
    st_illegal_parking_sv,
    st_crowd_sv,
    st_obj_attr_sv,
)

api_router = APIRouter()

api_router.include_router(
    login_routes.router,
    prefix="/login",
    tags=["LOGIN"],
    include_in_schema=False,
    # login is modified to be able to used in both postman and swagger
    # -> this default not work, just the login by icon lock in the swagger work
    # so I hide it (thanh.pt)
)
api_router.include_router(upload_routes.router, prefix="/file", tags=["FILE"])

api_router.include_router(user_routes.router, prefix="/user", tags=["USER"])

api_router.include_router(camera_routes.router, prefix="/camera", tags=["CAMERA"])

api_router.include_router(geo_unit_routes.router, prefix="/geo_unit", tags=["GEO UNIT"])
api_router.include_router(
    brand_camera_routes.router, prefix="/brand_camera", tags=["BRAND CAMERA"]
)

api_router.include_router(
    camera_type_ai_mapping_routes.router,
    prefix="/camera_type_ai_mapping",
    tags=["CAMERA TYPE AI MAPPING"],
)

api_router.include_router(company_routes.router, prefix="/company", tags=["COMPANY"])

api_router.include_router(server_routes.router, prefix="/server", tags=["SERVER"])

api_router.include_router(
    type_service_routes.router, prefix="/type_service", tags=["TYPE SERVICE"]
)

api_router.include_router(service_routes.router, prefix="/service", tags=["SERVICE"])

api_router.include_router(process_routes.router, prefix="/process", tags=["PROCESS"])

api_router.include_router(webhook_routes.router, prefix="/webhook", tags=["WEBHOOK"])

api_router.include_router(event_routes.router, prefix="/event", tags=["EVENT"])

api_router.include_router(vms_routes.router, prefix="/vms", tags=["VMS"])


api_router.include_router(
    setting_detect_items_forgotten_routes.router,
    prefix="/setting_detect_items_forgotten",
    tags=["SETTING DETECT ITEMS FORGOTTEN"],
)
api_router.include_router(
    setting_uniform_detection_routes.router,
    prefix="/setting_uniforms_detection",
    tags=["SETTING UNIFORM DETECTION"],
)

api_router.include_router(
    setting_uniform_config_company.router,
    prefix="/setting_uniform_config_company",
    tags=["SETTING UNIFORM CONFIG COMPANY"],
)

api_router.include_router(
    setting_tampering_routes.router,
    prefix="/setting_tampering",
    tags=["SETTING TAMPERRING"],
)

api_router.include_router(
    setting_camera_traffic_detection_routes.router,
    prefix="/setting_camera_traffic_detection",
    tags=["SETTING CAMERA TRAFFIC DETECTION"],
)

# lane violation, line violation, wrongway
lane_router = setting_ai_service_base_routes.get_routes(
    SettingLaneCreate, SettingLaneUpdate, st_lane_sv
)
api_router.include_router(
    lane_router, prefix="/setting_lane_violation", tags=["SETTING LANE VIOLATION"]
)

# leaving
leaving_router = setting_ai_service_base_routes.get_routes(
    SettingLeavingCreate, SettingLeavingUpdate, st_leaving_sv
)
api_router.include_router(
    leaving_router, prefix="/setting_leaving", tags=["SETTING LEAVING"]
)

# tripwire
tripwire_router = setting_ai_service_base_routes.get_routes(
    SettingTripwireCreate, SettingTripwireUpdate, st_tripwire_sv
)
api_router.include_router(
    tripwire_router, prefix="/setting_tripwire", tags=["SETTING TRIPWIRE"]
)

# loitering
loitering_router = setting_ai_service_base_routes.get_routes(
    SettingLoiteringCreate, SettingLoiteringUpdate, st_loitering_sv
)
api_router.include_router(
    loitering_router, prefix="/setting_loitering", tags=["SETTING LOITERING"]
)

# plate number
plate_number_router = setting_ai_service_base_routes.get_routes(
    SettingPlateNumberCreate, SettingPlateNumberUpdate, st_plate_number_sv
)
api_router.include_router(
    plate_number_router, prefix="/setting_plate_number", tags=["SETTING PLATE NUMBER"]
)

# illegal parking
illegal_parking_router = setting_ai_service_base_routes.get_routes(
    SettingIllegalParkingCreate, SettingIllegalParkingUpdate, st_illegal_parking_sv
)
api_router.include_router(
    illegal_parking_router,
    prefix="/setting_illegal_parking",
    tags=["SETTING ILLEGAL PARKING"],
)

# obj attr
obj_attr_router = setting_ai_service_base_routes.get_routes(
    SettingObjAttrCreate, SettingObjAttrUpdate, st_obj_attr_sv
)
api_router.include_router(
    obj_attr_router, prefix="/setting_obj_attr", tags=["SETTING OBJ ATTR"]
)


# crowd
crowd_router = setting_ai_service_base_routes.get_routes(
    SettingCrowdCreate, SettingCrowdUpdate, st_crowd_sv
)
api_router.include_router(crowd_router, prefix="/setting_crowd", tags=["SETTING CROWD"])

api_router.include_router(person_routers.router, prefix="/person", tags=["person"])
api_router.include_router(
    person_camera_router.router, prefix="/person_camera", tags=["person_camera"]
)
api_router.include_router(
    person_image_router.router, prefix="/person_image", tags=["person_image"]
)

api_router.include_router(
    video_analyze_routes.router, prefix="/video_analyze", tags=["VIDEO ANALYZE"]
)
