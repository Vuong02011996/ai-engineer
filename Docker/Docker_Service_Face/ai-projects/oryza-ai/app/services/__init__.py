# from app.services.camera_services import camera_services # noqa
from app.services.brand_camera_services import brand_camera_services # noqa
# from app.services.camera_type_ai_mapping_services import camera_type_ai_mapping_services # noqa
# from app.services.company_services import company_services # noqa
# from app.services.event_services import event_services # noqa
# from app.services.process_services import process_services # noqa
# from app.services.server_services import server_services # noqa
# from app.services.service_services import service_services # noqa
from app.services.type_service_services import type_service_services # noqa
# from app.services.user_services import user_services # noqa
# from app.services.webhook_services import webhook_services # noqa
from app.services.for3rd.geo_unit_services import geo_unit_services # noqa
from app.services.setting_ai_services import (
  setting_leaving_services as st_leaving_sv,
  setting_tripwire_services as st_tripwire_sv,
  setting_crowd_services as st_crowd_sv,
  setting_loitering_services as st_loitering_sv,
  setting_plate_number_services as st_plate_number_sv,
  setting_lane_violation_services as st_lane_violation_sv,
  setting_illegal_parking_services as st_illegal_parking_sv,
  setting_obj_attr_services as st_obj_attr_sv,
) # noqa
