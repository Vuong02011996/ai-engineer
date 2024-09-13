from app.models.brand_camera_model import BrandCamera  # noqa
from app.models.camera_model import Camera  # noqa
from app.models.camera_type_ai_mapping_model import CameraTypeAIMapping  # noqa
from app.models.company_model import Company  # noqa
from app.models.event_model import Event  # noqa
from app.models.process_model import Process  # noqa
from app.models.server_model import Server  # noqa
from app.models.service_model import Service  # noqa
from app.models.type_service_model import TypeService  # noqa
from app.models.user_model import User  # noqa
from app.models.webhook_model import Webhook  # noqa
from app.models.setting_ai_model import (
  SettingModelBase,
  SettingLeavingModel,
  SettingLoiteringModel,
  SettingTripwireModel,
  SettingCrowdModel,
  SettingLaneViolationModel,
  SettingPlateNumberModel,
  SettingIllegalParkingModel  ,
  SettingObjAttrModel
 ) # noqa
from app.models.for3rd.geo_unit_model import GeoUnit  # noqa
# Only use this if import to another group, for example: import model to service or route.
