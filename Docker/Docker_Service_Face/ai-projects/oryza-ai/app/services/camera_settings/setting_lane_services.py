from fastapi import HTTPException
from odmantic import ObjectId

from app.common.constants.filter_setting_crow_enum import FilterSettingCrow
from app.models import User
from app.models.camera_settings.setting_lane import SettingLane
from app.schemas.camera_settings.setting_lane_schemas import (
    SettingLaneCreate,
    SettingLaneUpdate,
)

from app.services.base_services import CRUDBase
from app.services.camera_services import camera_services
from app.services.camera_settings.base_setting_service import (
    get_all_info,
    get_count_info,
)


class CRUDSettingLane(CRUDBase[SettingLane, SettingLaneCreate, SettingLaneUpdate]):
    """
    This class is used to create, update, and get setting lane violation,
    include: lane violation, line violation, and wrong way driving.
    """

    def create_setting(self, res: SettingLaneCreate):
        # Check if camera not exist or camera already has setting
        camera_existed = camera_services.get_camera(id=res.camera_id)
        camera = self.get_by_camera(res.camera_id, res.key_ai)
        if camera:
            raise HTTPException(status_code=400, detail="Setting already exists")

        new_request = res.model_dump()
        new_request["camera"] = camera_existed
        del new_request["camera_id"]
        return super().create(obj_in=new_request)

    def update_setting(self, res: SettingLaneUpdate, setting_id: str):
        setting_existed = self.get(id=setting_id)
        if not setting_existed:
            raise HTTPException(status_code=400, detail="Setting not found")
        return super().update(obj_in=res, db_obj=setting_existed)

    def get_by_camera(self, camera_id: str, key_ai: str):
        return self.engine.find_one(
            SettingLane,
            SettingLane.camera == ObjectId(camera_id),
            SettingLane.key_ai == key_ai,
        )

    def get_all(self, company_id: str, key_ai: str):
        return list(
            self.engine.find(
                SettingLane,
                SettingLane.company_id == company_id,
                SettingLane.key_ai == key_ai,
            )
        )

    def get_all_info(
        self,
        user: User,
        page: int = 0,
        page_break: bool = False,
        data_search=None,
        filter: FilterSettingCrow = FilterSettingCrow.ALL,
    ):
        return get_all_info(
            user=user,
            page=page,
            page_break=page_break,
            data_search=data_search,
            filter=filter,
            name_table="setting_lane",
            engine=self.engine,
        )

    def get_count_info(
        self,
        user: User,
        data_search=None,
        filter: FilterSettingCrow = FilterSettingCrow.ALL,
    ):
        return get_count_info(
            user=user,
            data_search=data_search,
            filter=filter,
            name_table="setting_lane",
            engine=self.engine,
        )


setting_lane_services = CRUDSettingLane(SettingLane)
