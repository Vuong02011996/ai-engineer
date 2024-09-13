from datetime import datetime

from fastapi import HTTPException
from odmantic import ObjectId
from app.common.constants.rabbitmq_constants import (
    FACE_RECOGNITION_EXCHANGES,
    IDENTIFY_UNIFORMS_EXCHANGES,
    plate_number,
    illegal_parking,
    LANE_VIOLATION_EXCHANGES,
    LINE_VIOLATION_EXCHANGES,
    WRONG_WAY_EXCHANGES,
)
from app.core.config import settings
from app.models import Event, TypeService, User
from app.schemas.event_schemas import (
    EventCreate,
    EventUpdate,
    EventUpdateFace,
    SearchCondition,
)
from app.services.base_services import CRUDBase
from app.services.type_service_services import CRUDTypeService

type_service_services = CRUDTypeService(TypeService)


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    def get_event(self, id: str):
        event = super().get(id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    def get_by_type_service(
        self,
        user: User,
        type_service_id: str,
        page: int = 0,
        page_break: bool = False,
        start_time: str = None,
        end_time: str = None,
        data_search=None,
        filter=None,
    ):
        # Chuyển đổi các giá trị start_time và end_time từ chuỗi sang datetime
        start_datetime = datetime.fromisoformat(start_time) if start_time else None
        end_datetime = datetime.fromisoformat(end_time) if end_time else None

        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )
        type_service = type_service_services.get(id=type_service_id)
        if not type_service:
            raise HTTPException(status_code=404, detail="Type service not found")

        # Tạo bộ lọc truy vấn
        query = {"type_service": type_service.id, "company": user.company.id}

        if start_datetime and end_datetime:
            query["created"] = {
                "$gte": start_datetime,
                "$lte": end_datetime,
            }
        query = self.get_query_filter(query, filter, type_service.key)
        query = self.get_query_search(query, data_search, type_service.key)
        # Thực hiện truy vấn MongoDB với các bộ lọc và sắp xếp
        events = self.engine.find(
            self.model,
            query,
            **offset,
            sort=self.model.created.desc(),
        )
        return events

    def get_count(
        self,
        user: User,
        type_service_id: str,
        start_time: str = None,
        end_time: str = None,
        data_search=None,
        filter=None,
    ):
        type_service = type_service_services.get_type_service(id=type_service_id)
        start_datetime = datetime.fromisoformat(start_time) if start_time else None
        end_datetime = datetime.fromisoformat(end_time) if end_time else None
        # Tạo bộ lọc truy vấn
        query = {"type_service": type_service.id, "company": user.company.id}

        if start_datetime and end_datetime:
            query["created"] = {
                "$gte": start_datetime,
                "$lte": end_datetime,
            }
        query = self.get_query_filter(query, filter, type_service.key)
        query = self.get_query_search(query, data_search, type_service.key)
        count = self.engine.count(self.model, query)
        return count

    def get_query_filter(self, query, filter: str, type_service_key: str):
        if type_service_key == FACE_RECOGNITION_EXCHANGES:
            if filter and filter != "ALL":
                if filter == "UNKNOWN":
                    query["data.user_id"] = "Unknown"
                else:
                    query["data.user_id"] = {"$ne": "Unknown"}
        elif type_service_key == IDENTIFY_UNIFORMS_EXCHANGES:
            if filter:
                query["data.error_code"] = filter
        return query

    def get_query_search(self, query, data_search: str, type_service_key: str):
        if data_search:
            common_queries = [
                {"data.camera_ip": {"$regex": data_search, "$options": "i"}},
                {"data.camera_name": {"$regex": data_search, "$options": "i"}},
            ]
            if type_service_key == FACE_RECOGNITION_EXCHANGES:
                query["$or"] = [
                    {"data.name": {"$regex": data_search, "$options": "i"}},
                    {"data.timestamp": {"$regex": data_search, "$options": "i"}},
                ] + common_queries
            elif type_service_key == IDENTIFY_UNIFORMS_EXCHANGES:
                query["$or"] = [
                    {"data.name": {"$regex": data_search, "$options": "i"}},
                ] + common_queries
            elif type_service_key == plate_number:
                query["$or"] = [
                    {"data.license_plate": {"$regex": data_search, "$options": "i"}},
                    {"data.brand_name": {"$regex": data_search, "$options": "i"}},
                    {"data.vehicle_color": {"$regex": data_search, "$options": "i"}},
                    {"data.vehicle_type": {"$regex": data_search, "$options": "i"}},
                ] + common_queries
            elif type_service_key == illegal_parking:
                query["$or"] = [
                    {"data.license_plate": {"$regex": data_search, "$options": "i"}},
                    {"data.status": {"$regex": data_search, "$options": "i"}},
                ] + common_queries
            elif type_service_key in [
                LANE_VIOLATION_EXCHANGES,
                LINE_VIOLATION_EXCHANGES,
                WRONG_WAY_EXCHANGES,
            ]:
                query["$or"] = [
                    {"data.license_plate": {"$regex": data_search, "$options": "i"}},
                ] + common_queries
            else:
                query["$or"] = common_queries
        return query

    def update_loitering_detection(
        self, end_time, image_end, id_camera, track_id, duration_time
    ):
        try:
            query = {
                "camera": id_camera,
                "data.track_id": track_id,
                "data.duration_time": -1,
            }
            event = self.engine.find_one(self.model, query)
            if event:
                event.data["end_time"] = end_time
                event.data["image_end"] = image_end
                event.data["duration_time"] = duration_time
                self.engine.save(event)
        except Exception as e:
            print("error", e)

    def update_illegal_parking(
        self, end_time, image_end, id_camera, track_id, duration_time, status
    ):
        try:
            query = {
                "camera": id_camera,
                "data.track_id": track_id,
            }
            event = self.engine.find_one(self.model, query)
            if event:
                event.data["end_time"] = end_time
                event.data["image_end"] = image_end
                event.data["duration_time"] = duration_time
                event.data["status"] = status
                self.engine.save(event)
        except Exception as e:
            print("error", e)

    def update_face_recognition(self, data: EventUpdateFace):
        try:
            user_id = data.user_id
            name = data.name
            list_id_event = data.list_id_event
            # convert list_id_event to ObjectId
            list_id_event = [ObjectId(id) for id in list_id_event]
            query = {
                "_id": {"$in": list_id_event},
            }
            events = self.engine.find(self.model, query)
            for event in events:
                event.data["user_id"] = user_id
                event.data["name"] = name
                self.engine.save(event)
            return {"message": "success"}
        except Exception as e:
            print("error", e)
            return {"message": "error"}

    def get_by_camera(self, *, camera_id: str):
        return list(
            self.engine.find(self.model, self.model.camera == ObjectId(camera_id))
        )

    def remove_field_camera(self, *, camera_id: str):
        """When Camera is removed, Change field 'camera' of all event related to that camera to a default object"""
        related_events = self.get_by_camera(camera_id=camera_id)
        for event in related_events:
            event.camera = ""

    def get_by_type_service_raw(self, *, type_service_id: str):
        return list(
            self.engine.find(
                self.model, self.model.type_service == ObjectId(type_service_id)
            )
        )

    def remove_field_type_service(self, *, type_service_id: str, null_obj: str):
        "When a type service is removed, change field 'type_service' of all event related to that type service to a default object"
        related_events = self.get_by_type_service_raw(type_service_id=type_service_id)
        for event in related_events:
            super().update(db_obj=event, obj_in={"type_service": null_obj})

    def get_record(self, id: str):
        from app.services.camera_services import camera_services
        from app.services.vms_services import vms_services

        event = super().get(id=id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        camera_id = event.camera
        camera = camera_services.get(id=camera_id)
        if not camera:
            raise HTTPException(status_code=404, detail="Camera not found")

        camera_id_vms = camera.other_info.get("id_vms")
        if not camera_id_vms:
            raise HTTPException(status_code=404, detail="Camera not found in VMS")

        timestamp = event.data.get("timestamp")
        timestamp = int(timestamp) - 5  # 5 seconds before the event
        # vms
        vms = vms_services.get_by_company_id(company_id=str(camera.company.id))
        ip_address = vms.ip_address.split("//")[1]
        ip_address = f"https://{vms.username}:{vms.password}@{ip_address}"
        url = f"{ip_address}:{vms.port}/media/{camera_id_vms}.webm?pos={timestamp}&duration=10"
        return {"data": url}

    def search_event_images(self, search_condition: SearchCondition):
        """ODMantic not have projection yet. So we must get all event, then loop for images"""
        from bson import datetime as bson_datetime
        from app.services.camera_services import camera_services

        # check if camera or type_service is not exist
        camera_services.get_camera(id=search_condition.camera_id)
        if search_condition.type_service_id:
            type_service_services.get_type_service(id=search_condition.type_service_id)

        # Check if time is valid
        if search_condition.start_time > search_condition.end_time:
            raise HTTPException(
                status_code=400, detail="Start time must be before end time"
            )
        start_time = bson_datetime.datetime.fromtimestamp(search_condition.start_time)
        end_time = bson_datetime.datetime.fromtimestamp(search_condition.end_time)
        query_conditions = {
            "created": {"$gte": start_time, "$lte": end_time},
            "camera": search_condition.camera_id,
        }
        if search_condition.type_service_id:
            query_conditions["type_service"] = ObjectId(
                search_condition.type_service_id
            )
        print("query_conditions: ", query_conditions)
        events = self.engine.find(
            self.model,
            query_conditions,
        )
        event_images = []
        for event in events:
            data = event.data
            event_images.append(
                {
                    key: value
                    for key, value in {
                        "full_img": data.get("full_img"),
                        "crop_plate": data.get("crop_plate"),
                        "crop_face": data.get("crop_face"),
                        "image_url": data.get("image_url"),
                    }.items()
                    if value is not None and value is not False and value != ""
                }
            )
        return event_images

    async def download_images_from_event(self, search_condition: SearchCondition):
        import os
        import random
        from requests import request
        import shutil
        from app.common.utils.minio_services import minio_services
        import string

        request_time = datetime.now().strftime("%Y%m%d%H%M%S")
        result_folder = f"{request_time}_{random.randint(100, 999)}_{random.choice(string.ascii_lowercase)}"
        result_folder = f"./temp/download_images/{result_folder}"
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        list_folder = ["full_img", "crop_plate", "crop_face", "image_url"]
        for folder in list_folder:
            folder_path = f"{result_folder}/{folder}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        items: list[dict] = self.search_event_images(search_condition)
        for item in items:
            for key in list_folder:
                url: str = item.get(key)
                if url:
                    response = request("GET", url)
                    if response.status_code == 200:
                        with open(
                            f"{result_folder}/{key}/{url.split('/')[-1]}", "wb"
                        ) as f:
                            f.write(response.content)

        # Check if the folder is empty
        for folder in list_folder:
            if not os.listdir(f"{result_folder}/{folder}"):
                os.rmdir(f"{result_folder}/{folder}")

        shutil.make_archive(result_folder, "zip", result_folder)
        retry_attempts = 2  # Total attempts: 1 initial + 1 retry
        for attempt in range(retry_attempts):
            try:
                rs = minio_services.upload_file(
                    f"{result_folder}.zip", f"{result_folder.split('/')[-1]}.zip"
                )
                break  # Exit the loop if upload is successful
            except Exception:
                if attempt < retry_attempts - 1:
                    print(f"Upload failed, retrying... (attempt {attempt + 1})")
                else:
                    raise HTTPException(
                        status_code=500, detail="Upload failed, try again later"
                    )
        try:
            shutil.rmtree(result_folder)
            os.remove(f"{result_folder}.zip")
        except Exception as e:
            print("Error remove temp folder: ", e)
        return rs

    def get_plate_number(self, camera_id: str, start_time: int, end_time: int):
        try:
            if start_time > end_time:
                raise HTTPException(
                    status_code=400, detail="Start time must be before end time"
                )
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid timestamp format")

        plate_number_type_service = type_service_services.get_by_key(plate_number)
        if not plate_number_type_service:
            raise HTTPException(
                status_code=404, detail="Plate number type service not found"
            )
        print("\ncamera_id: ", camera_id)
        print("\nplate_number_type_service: ", plate_number_type_service)
        query = {
            "type_service": plate_number_type_service.id,
            "camera": camera_id,
            "data.timestamp": {
                "$gte": start_time,
                "$lte": end_time,
            },
        }
        print("\nquery: ", query)
        events = self.engine.find(self.model, query)
        events = list(events)
        if len(events) == 0:
            raise HTTPException(status_code=404, detail="No plate number found")
        result = []
        for event in events:
            data = event.data
            result.append(
                {
                    "license_plate": data.get("license_plate"),
                    "timestamp": data.get("timestamp"),
                }
            )
        return result


event_services = CRUDEvent(Event)
