from app.schemas.base_schemas import BaseSchema, Count, Msg  # noqa
from app.schemas.brand_camera_schemas import BrandCameraCreate, BrandCameraUpdate  # noqa
from app.schemas.camera_schemas import (
  CameraCreate, CameraUpdate,
  ListCameraOut
)  # noqa
from app.schemas.company_schemas import CompanyCreate, CompanyUpdate  # noqa
from app.schemas.event_schemas import EventCreate, EventUpdate  # noqa
from app.schemas.process_schemas import ProcessCreate, ProcessUpdate  # noqa
from app.schemas.server_schemas import ServerCreate, ServerUpdate  # noqa
from app.schemas.service_schemas import ServiceCreate, ServiceUpdate  # noqa
from app.schemas.user_schemas import UserCreate, UserUpdate  # noqa
from app.schemas.type_service_schemas import TypeServiceCreate, TypeServiceUpdate  # noqa
from app.schemas.webhook_schemas import WebhookCreate, WebhookUpdate  # noqa
from app.schemas.setting_ai_schemas import (
  SettingBase, SettingCreateBase, SettingUpdateBase,
  SettingLeavingCreate, SettingLeavingUpdate,
  SettingLoiteringCreate, SettingLoiteringUpdate, 
  SettingTripwireCreate, SettingTripwireUpdate,
  SettingCrowdCreate, SettingCrowdUpdate,
  SettingLaneViolationCreate, SettingLaneViolationUpdate,
  SettingPlateNumberCreate, SettingPlateNumberUpdate,
  SettingIllegalParkingCreate, SettingIllegalParkingUpdate,
  SettingObjAttrCreate, SettingObjAttrUpdate
) # noqa
from app.schemas.for3rd.geo_unit_schemas import (
  GeoUnitCreate, GeoUnitUpdate, GeoUnitOut,
  GeoUnitGet, GeoUnitGetDetail,
  ListGeoUnitOut
) # noqa
# Only use this if import to another group, for example: import schema to service or route.
