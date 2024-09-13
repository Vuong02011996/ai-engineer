import os

import cv2
from fastapi import HTTPException

from app.common.constants.filter_setting_crow_enum import FilterSettingCrow
from app.common.utils.minio_services import MinioServices
from app.core.config import settings
from app.models import User, Camera
from app.services.camera_services import camera_services


def get_image_by_id_camera(id_camera: str, type="crowd"):
    try:
        camera = camera_services.get(id=id_camera)
        if not camera:
            raise HTTPException(status_code=400, detail="Camera not found")
        # if camera.rtsp_vms is not None and camera.rtsp_vms != "":
        #     rtsp = camera.rtsp_vms
        # else:
        rtsp_auth = f"rtsp://{camera.username}:{camera.password}@"
        if rtsp_auth not in camera.rtsp:
            rtsp = rtsp_auth + camera.rtsp.split("rtsp://")[1]
        else:
            rtsp = camera.rtsp
        minio_services = MinioServices()
        cap = cv2.VideoCapture(rtsp)
        if not cap.isOpened():
            raise HTTPException(status_code=400, detail="Camera not open")
        ret, frame = cap.read()
        if not ret:
            raise HTTPException(status_code=400, detail="Camera not open")
        cap.release()
        if not os.path.exists("./temp"):
            os.makedirs("./temp")
        name = type + "_" + id_camera
        path_save = f"./temp/{name}.jpg"
        cv2.imwrite(path_save, frame)
        url = minio_services.upload_file(f"./temp/{name}.jpg", f"{name}.jpg")
        if os.path.exists(path_save):
            os.remove(path_save)
        return url
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error get image by id camera, {e}"
        )


def get_all_info(
    user: User,
    page: int = 0,
    page_break: bool = False,
    data_search=None,
    filter: FilterSettingCrow = FilterSettingCrow.ALL,
    name_table: str = "setting_crowd_detection",
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


def get_count_info(
    user: User,
    data_search=None,
    filter: FilterSettingCrow = FilterSettingCrow.ALL,
    name_table: str = "setting_crowd_detection",
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
        {"$sort": {"created_at": -1}},
    ]

    data = engine.get_collection(Camera).aggregate(pipeline)
    return len(list(data))
