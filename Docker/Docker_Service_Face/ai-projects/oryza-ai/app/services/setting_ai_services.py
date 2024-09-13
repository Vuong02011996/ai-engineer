from fastapi import HTTPException
from odmantic import ObjectId
from typing import Optional, TypeVar, Type
from app.common.constants.filter_setting_crow_enum import FilterSettingCrow
from app.models import (
    User,
    Camera,
    SettingModelBase,
    SettingLeavingModel,
    SettingLoiteringModel,
    SettingTripwireModel,
    SettingCrowdModel,
    SettingLaneViolationModel,
    SettingPlateNumberModel,
    SettingIllegalParkingModel,
    SettingObjAttrModel,
)
from app.schemas import (
    SettingCreateBase,
    SettingUpdateBase,
    SettingLeavingCreate,
    SettingLeavingUpdate,
    SettingLoiteringCreate,
    SettingLoiteringUpdate,
    SettingTripwireCreate,
    SettingTripwireUpdate,
    SettingCrowdCreate,
    SettingCrowdUpdate,
    SettingLaneViolationCreate,
    SettingLaneViolationUpdate,
    SettingPlateNumberCreate,
    SettingPlateNumberUpdate,
    SettingObjAttrCreate,
    SettingObjAttrUpdate,
)

from app.services.base_services import CRUDBase
from app.services.camera_services import camera_services
from app.core.config import settings


def _get_all_info(
    user: User,
    page: int = 0,
    page_break: bool = False,
    data_search=None,
    filter: FilterSettingCrow = FilterSettingCrow.ALL,
    name_table: str = "setting_crowd_detection",
    key_ai: Optional[str] = None,
    engine=None,
):
    filter_setting = {}
    if filter == FilterSettingCrow.NO_SETTING:
        filter_setting = {"settings": {"$size": 0}}
    if filter == FilterSettingCrow.SETTING:
        filter_setting = {"settings": {"$ne": []}}
    search = {}
    if data_search:
        search = {
            "$or": [
                {"name": {"$regex": data_search, "$options": "i"}},
                {"ip_address": {"$regex": data_search, "$options": "i"}},
            ]
        }
    pipeline = [
        {
            "$lookup": {
                "from": name_table,
                "localField": "_id",
                "foreignField": "camera",
                "as": "settings",
            }
        },
        {"$match": {"company": user.company.id}},
        {"$match": filter_setting},
        {"$match": search},
        {"$sort": {"created": -1}},
    ]

    if key_ai:
        pipeline.append({"$match": {"settings.key_ai": key_ai}})
    if page_break:
        items_per_page = settings.MULTI_MAX
        pipeline.extend([{"$skip": page * items_per_page}, {"$limit": items_per_page}])

    data = engine.get_collection(Camera).aggregate(pipeline)
    data = list(data)
    result = []
    for i in data:
        setting = i["settings"][0] if i["settings"] else None
        if setting is not None:
            setting["id"] = str(setting["_id"])
            del setting["_id"]
            del setting["camera"]
        result.append(
            {
                "id": str(i["_id"]),
                "name": i["name"],
                "rtsp": i["rtsp"],
                "ip_address": i["ip_address"],
                "port": i["port"],
                "username": i["username"],
                "password": i["password"],
                "setting": i["settings"][0] if i["settings"] else None,
            }
        )
    return result


def _get_count_info(
    user: User,
    data_search=None,
    filter: FilterSettingCrow = FilterSettingCrow.ALL,
    name_table: str = "setting_crowd_detection",
    engine=None,
    key_ai: Optional[str] = None,
):
    filter_setting = {}
    if filter == FilterSettingCrow.NO_SETTING:
        filter_setting = {"settings": {"$size": 0}}
    if filter == FilterSettingCrow.SETTING:
        filter_setting = {"settings": {"$ne": []}}
    search = {}
    if data_search:
        search = {
            "$or": [
                {"name": {"$regex": data_search, "$options": "i"}},
                {"ip_address": {"$regex": data_search, "$options": "i"}},
            ]
        }
    pipeline = [
        {
            "$lookup": {
                "from": name_table,
                "localField": "_id",
                "foreignField": "camera",
                "as": "settings",
            }
        },
        {"$match": {"company": user.company.id}},
        {"$match": filter_setting},
        {"$match": search},
        {"$sort": {"created_at": -1}},
    ]
    if key_ai:
        pipeline.append({"$match": {"settings.key_ai": key_ai}})
    data = engine.get_collection(Camera).aggregate(pipeline)
    return len(list(data))


ModelType = TypeVar("ModelType", bound=SettingModelBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SettingCreateBase)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SettingUpdateBase)


class CRUDSettingBase(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    name_table = ""

    def __init__(self, model: Type[ModelType]):
        super().__init__(model=model)

    def create_setting(self, res: SettingCreateBase):
        # Check if camera not exist or camera already has setting
        camera_existed = camera_services.get_camera(id=res.camera_id)
        camera = self.get_by_camera(res.camera_id, res.key_ai)
        if camera:
            raise HTTPException(status_code=400, detail="Setting already exists")

        new_request = res.model_dump()
        new_request["camera"] = camera_existed
        del new_request["camera_id"]
        print(new_request)
        return super().create(obj_in=new_request)

    def update_setting(self, res: SettingUpdateBase, setting_id: str):
        setting_existed = self.get(setting_id)
        if not setting_existed:
            raise HTTPException(status_code=400, detail="Setting not found")
        return super().update(obj_in=res, db_obj=setting_existed)

    def get_by_camera(self, camera_id: str, key_ai: Optional[str] = None):
        # query = {SettingModelBase.camera: ObjectId(camera_id)}
        query_conditions = {"camera": ObjectId(camera_id)}
        if key_ai:
            # query[SettingModelBase.key_ai] = key_ai
            query_conditions["$and"] = [
                {"key_ai": key_ai},
            ]
        return self.engine.find_one(self.model, query_conditions)

    def get_all(self, company_id: str, key_ai: Optional[str] = None):
        print("get_all", company_id, key_ai)
        query_conditions = {"company_id": company_id}
        if key_ai:
            query_conditions["$and"] = [
                {"key_ai": key_ai},
            ]
        return self.engine.find(self.model, query_conditions)

    def get_all_info(
        self,
        user: User,
        page: int = 0,
        page_break: bool = False,
        data_search=None,
        key_ai: Optional[str] = None,
        filter: FilterSettingCrow = FilterSettingCrow.ALL,
    ):
        return _get_all_info(
            user=user,
            page=page,
            page_break=page_break,
            data_search=data_search,
            filter=filter,
            name_table=self.name_table,
            engine=self.engine,
            key_ai=key_ai,
        )

    def get_count_info(
        self,
        user: User,
        data_search=None,
        key_ai: Optional[str] = None,
        filter: FilterSettingCrow = FilterSettingCrow.ALL,
    ):
        return _get_count_info(
            user=user,
            data_search=data_search,
            filter=filter,
            name_table=self.name_table,
            engine=self.engine,
            key_ai=key_ai,
        )


# Inheriting base setting
class CRUDSettingLeaving(
    CRUDSettingBase[SettingLeavingModel, SettingLeavingCreate, SettingLeavingUpdate],
):
    name_table = "setting_leaving"

    def __init__(self, model: SettingLeavingModel):
        self.model = model
        super().__init__(model=model)


class CRUDSettingLoitering(
    CRUDSettingBase[
        SettingLoiteringModel, SettingLoiteringCreate, SettingLoiteringUpdate
    ],
):
    name_table = "setting_loitering"

    def __init__(self, model: SettingLoiteringModel):
        self.model = model
        super().__init__(model=model)


class CRUDSettingTripwire(
    CRUDSettingBase[SettingTripwireModel, SettingTripwireCreate, SettingTripwireUpdate],
):
    name_table = "setting_tripwire"

    def __init__(self, model: SettingTripwireModel):
        self.model = model
        super().__init__(model=model)


class CRUDSettingCrowd(
    CRUDSettingBase[SettingCrowdModel, SettingCrowdCreate, SettingCrowdUpdate],
):
    name_table = "setting_crowd"

    def __init__(self, model: SettingCrowdModel):
        self.model = model
        super().__init__(model=model)


class CRUDSettingLaneViolation(
    CRUDSettingBase[
        SettingLaneViolationModel,
        SettingLaneViolationCreate,
        SettingLaneViolationUpdate,
    ],
):
    name_table = "setting_lane_violation"

    def __init__(self, model: SettingLaneViolationModel):
        self.model = model
        super().__init__(model=model)


class CRUDSettingPlateNumber(
    CRUDSettingBase[
        SettingPlateNumberModel, SettingPlateNumberCreate, SettingPlateNumberUpdate
    ],
):
    name_table = "setting_plate_number"

    def __init__(self, model: SettingPlateNumberModel):
        self.model = model
        super().__init__(model=model)


class CRUDSettingIllegalParking(
    CRUDSettingBase[SettingIllegalParkingModel, SettingCreateBase, SettingUpdateBase],
):
    name_table = "setting_illegal_parking"

    def __init__(self, model: SettingIllegalParkingModel):
        self.model = model
        super().__init__(model=model)


class CRUDSettingObjAttr(
    CRUDSettingBase[SettingModelBase, SettingObjAttrCreate, SettingObjAttrUpdate],
):
    name_table = "setting_obj_attr"

    def __init__(self, model: SettingModelBase):
        self.model = model
        super().__init__(model=model)


# Define Setting services
setting_leaving_services = CRUDSettingLeaving(SettingLeavingModel)
setting_loitering_services = CRUDSettingLoitering(SettingLoiteringModel)
setting_tripwire_services = CRUDSettingTripwire(SettingTripwireModel)
setting_crowd_services = CRUDSettingCrowd(SettingCrowdModel)
setting_lane_violation_services = CRUDSettingLaneViolation(SettingLaneViolationModel)
setting_plate_number_services = CRUDSettingPlateNumber(SettingPlateNumberModel)
setting_illegal_parking_services = CRUDSettingIllegalParking(SettingIllegalParkingModel)
setting_obj_attr_services = CRUDSettingObjAttr(SettingObjAttrModel)
