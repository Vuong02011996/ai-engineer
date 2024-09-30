from fastapi import HTTPException
from odmantic import ObjectId

from app.common.constants.filter_setting_crow_enum import FilterSettingCrow
from app.models import User
from app.models.camera_settings.setting_camera_traffic_detection import SettingCameraTrafficDetection
from app.schemas.camera_settings.setting_camera_trafic_schemas import SettingCameraTrafficCreate, \
    SettingCameraTrafficUpdate
from app.services.base_services import CRUDBase
from app.services.camera_services import camera_services
from app.services.camera_settings.base_setting_service import get_all_info, get_count_info


class CRUDSettingCameraTrafficService(
    CRUDBase[
        SettingCameraTrafficDetection, SettingCameraTrafficCreate, SettingCameraTrafficUpdate
    ]
):
    def create_setting(self, res: SettingCameraTrafficCreate):
        camera_Exits = camera_services.get(id=res.camera_id)
        if not camera_Exits:
            raise HTTPException(status_code=400, detail="Camera not found")
        camera = self.get_by_id_camera(id_camera=res.camera_id)
        if camera:
            raise HTTPException(
                status_code=400, detail="Setting  already exists"
            )

        new_request = res.model_dump()
        new_request["camera"] = camera_Exits
        del new_request["camera_id"]
        return super().create(obj_in=new_request)

    def update_setting(
            self, res: SettingCameraTrafficUpdate, id: str
    ):
        setting_exit = self.get(id=id)
        if not setting_exit:
            raise HTTPException(status_code=400, detail="Setting not found")

        return super().update(obj_in=res, db_obj=setting_exit)

    def get_by_id_camera(self, id_camera: str):
        return self.engine.find_one(
            SettingCameraTrafficDetection, SettingCameraTrafficDetection.camera == ObjectId(id_camera)
        )

    def get_all(self, id_company: str):
        return list(
            self.engine.find(
                SettingCameraTrafficDetection, SettingCameraTrafficDetection.id_company == id_company
            )
        )

    def get_all_info(self, user: User, page: int = 0, page_break: bool = False, data_search=None,
                     filter: FilterSettingCrow = FilterSettingCrow.ALL
                     ):

        return get_all_info(user=user, page=page, page_break=page_break, data_search=data_search, filter=filter,
                            name_table="setting_camera_traffic_detection", engine=self.engine)

    def get_count_info(self, user: User, data_search=None, filter: FilterSettingCrow = FilterSettingCrow.ALL):
        return get_count_info(user=user, data_search=data_search, filter=filter,
                              name_table="setting_camera_traffic_detection",
                              engine=self.engine)


setting_camera_traffic_services = CRUDSettingCameraTrafficService(SettingCameraTrafficDetection)