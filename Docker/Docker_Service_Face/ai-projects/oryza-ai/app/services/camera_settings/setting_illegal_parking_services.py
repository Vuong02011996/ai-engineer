from fastapi import HTTPException
from odmantic import ObjectId

from app.common.constants.filter_setting_crow_enum import FilterSettingCrow
from app.models import User
from app.models.camera_settings.setting_illegal_parking import SettingIllegalParking
from app.schemas.camera_settings.setting_illegal_parking_schemas import (
    SettingIllegalParkingCreate,
    SettingIllegalParkingUpdate,
)

from app.services.base_services import CRUDBase
from app.services.camera_services import camera_services
from app.services.camera_settings.base_setting_service import (
    get_all_info,
    get_count_info,
)


class CRUDSettingIllegalParking(
    CRUDBase[
        SettingIllegalParking, SettingIllegalParkingCreate, SettingIllegalParkingUpdate
    ]
):
    def create_setting(self, res: SettingIllegalParkingCreate):
        camera_exist = camera_services.get(id=res.camera_id)
        if not camera_exist:
            raise HTTPException(status_code=400, detail="Camera not found")
        camera = self.get_by_id_camera(id_camera=res.camera_id)
        if camera:
            raise HTTPException(status_code=400, detail="Setting  already exists")

        new_request = res.model_dump()
        new_request["camera"] = camera_exist
        del new_request["camera_id"]
        return super().create(obj_in=new_request)

    def update_setting(self, res: SettingIllegalParkingUpdate, id: str):
        setting_exist = self.get(id=id)
        if not setting_exist:
            raise HTTPException(status_code=400, detail="Setting not found")

        return super().update(obj_in=res, db_obj=setting_exist)

    def get_by_id_camera(self, id_camera: str):
        return self.engine.find_one(
            SettingIllegalParking, SettingIllegalParking.camera == ObjectId(id_camera)
        )

    def get_all(self, id_company: str):
        return list(
            self.engine.find(
                SettingIllegalParking, SettingIllegalParking.id_company == id_company
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
            name_table="setting_illegal_parking",
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
            name_table="setting_illegal_parking",
            engine=self.engine,
        )


setting_illegal_parking_services = CRUDSettingIllegalParking(SettingIllegalParking)
