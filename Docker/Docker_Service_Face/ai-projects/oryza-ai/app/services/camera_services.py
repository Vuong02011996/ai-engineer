from fastapi import HTTPException
from odmantic import ObjectId
from odmantic.query import match
import json

from app.common.constants.enums import TypeServiceEnum
from app.common.constants.rabbitmq_constants import FACE_RECOGNITION_EXCHANGES
from app.models import Camera, BrandCamera, CameraTypeAIMapping, User, Service
from app.schemas import CameraCreate, CameraUpdate
from app.schemas.camera_schemas import GenerateRTSP
from app.services.camera_type_ai_mapping_services import CRUDCameraTypeAIMapping
from app.services.base_services import CRUDBase
from app.services.brand_camera_services import CRUDBrandCamera
from app.core.config import settings
from app.services.event_services import type_service_services

brand_camera_services = CRUDBrandCamera(BrandCamera)
mapping_services = CRUDCameraTypeAIMapping(CameraTypeAIMapping)


class CRUDCamera(CRUDBase[Camera, CameraCreate, CameraUpdate]):
    def count_camera(self, *, user: User, data_search=None) -> int:
        query_conditions = {"company": user.company.id}

        if data_search:
            regex_search = {"$regex": f".*{data_search}.*", "$options": "i"}
            query_conditions["$or"] = [
                {"name": regex_search},
                {"ip_address": regex_search},
            ]

        return self.engine.count(Camera, query_conditions)

    def get_by_face_ai(self, *, company_id, data_search: str = None):
        type_service_face = type_service_services.get_type_service_by_key(
            FACE_RECOGNITION_EXCHANGES
        )
        search = {"$match": {}}
        if data_search:
            search = {
                "$match": {
                    "$or": [
                        {"ip_address": {"$regex": data_search, "$options": "i"}},
                    ]
                }
            }
        pipeline = [
            {
                "$lookup": {
                    "from": "camera_type_ai_mapping",
                    "localField": "_id",
                    "foreignField": "camera",
                    "as": "camera_mapping",
                }
            },
            {"$unwind": "$camera_mapping"},
            {"$match": {"camera_mapping.type_service": type_service_face.id}},
            {"$match": {"company": company_id}},
            # {"$match": {"type": TypeServiceEnum.ai_service}},
            {"$match": {"is_ai": True}},
            search,
            {
                "$lookup": {
                    "from": "brand_camera",
                    "localField": "brand_camera",
                    "foreignField": "_id",
                    "as": "brand_camera",
                }
            },
        ]
        data = self.engine.get_collection(Camera).aggregate(pipeline)
        data = list(data)
        result = []
        for item in data:
            item["id"] = str(item["_id"])
            del item["_id"]
            del item["company"]
            # del item["brand_camera"]
            del item["camera_mapping"]
            brand_camera = {}
            if len(item["brand_camera"]) > 0:
                brand_camera["id"] = str(item["brand_camera"][0]["_id"])
                brand_camera["name"] = item["brand_camera"][0]["name"]
                brand_camera["key"] = item["brand_camera"][0]["key"]
            item["brand_camera"] = brand_camera
            item["type_camera"] = "Camera AI"
            result.append(item)

        service_faces = self.engine.find(
            Service,
            Service.type_service == type_service_face.id,
            Service.type == TypeServiceEnum.ai_service,
        )
        service_faces = list(service_faces)
        if len(service_faces) > 0:
            service_face = service_faces[0]
            if data_search:
                if (
                    data_search.lower() not in service_face.server.ip_address.lower()
                    and data_search.lower() not in service_face.name.lower()
                ):
                    return result
            data = {
                "brand_camera": {
                    "id": "60f3b3b3b3b3b3b3b3b3b3b3",
                    "name": "Face Service",
                    "key": "FACE_SERVICE",
                },
                "created": service_face.created,
                "ip_address": service_face.server.ip_address,
                "is_ai": True,
                "modified": service_face.modified,
                "name": "Face Service",
                "other_info": {},
                "password": "",
                "port": service_face.port,
                "rtsp": "",
                "username": "",
                "id": str(service_face.id),
                "type_camera": "Service AI",
            }
            result.append(data)

        return result

    def get_camera(self, *, id: str):
        """Get camera by id. If camera not found, raise error."""
        camera = super().get(id)
        if not camera:
            raise HTTPException(status_code=404, detail="Camera not found")
        # if str(camera.company.id) != str(user.company.id):
        #     raise HTTPException(status_code=403, detail="Not enough permissions")
        return camera

    def get_cameras(
        self, *, user: User, page: int = 0, page_break: bool = False, data_search=None
    ):
        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )

        query_conditions = {"company": user.company.id}

        if data_search:
            regex_search = {"$regex": f".*{data_search}.*", "$options": "i"}
            query_conditions["$or"] = [
                {"name": regex_search},
                {"ip_address": regex_search},
            ]

        return self.engine.find(
            Camera,
            query_conditions,
            **offset,
            sort=Camera.created.desc(),
        )

    def get_cameras_by_company(self, user: User, company_id: str):
        """Get all cameras by company_id. If user is superuser, return all cameras."""
        if user.is_superuser or str(user.company.id) == company_id:
            return list(
                self.engine.find(Camera, Camera.company == ObjectId(company_id))
            )

    def get_camera_by_ip_and_port_rtsp(
        self, ip_address: str, port_rtsp: int
    ) -> Camera | None:
        """Get camera by ip_address and port_rtsp. (ip_address, port_rtsp) is unique"""
        camera: Camera = self.engine.find_one(
            Camera,
            Camera.ip_address == ip_address,
            match(Camera.rtsp, f".*:{port_rtsp}/.*"),
        )
        return camera

    def get_port_rtsp(self, rtsp: str) -> int:
        """
        Get port from rtsp. Rtsp alway have port.
        For example: rtsp://192.168.111.6:80/ -> 80: int
        """
        return rtsp.split(":")[-1].split("/")[0]

    def check_unique_camera(self, camera_id: str, ip_address: str, port_rtsp: int):
        """
        Check if camera already exists. Camera is unique by (ip_address, port_rtsp)
        """
        camera: Camera = self.get_camera_by_ip_and_port_rtsp(
            ip_address=ip_address, port_rtsp=port_rtsp
        )
        if camera and str(camera.id) != camera_id:
            raise HTTPException(status_code=400, detail="Camera already exists")

    def update_id_vms(self, camera: Camera, other_info: dict):
        """
        Update id_vms of camera. If camera already exists, update other_info, return camera.
        """
        if other_info and camera.other_info["id_vms"] != other_info["id_vms"]:
            # print("Update camera", str(camera.id), "with id_vms", other_info["id_vms"])
            # print('\ncamera.other_info["id_vms"]', camera.other_info["id_vms"])
            # print("\nob_in.other_info['id_vms']", other_info["id_vms"])
            super().update(db_obj=camera, obj_in={"other_info": other_info})

    def create_camera(self, *, user: User, obj_in: CameraCreate) -> Camera:
        new_request = obj_in.model_dump()
        # Check if camera already exists: ip_address, port rtsp
        port_rtsp = self.get_port_rtsp(new_request["rtsp"])
        camera = self.get_camera_by_ip_and_port_rtsp(
            ip_address=new_request["ip_address"], port_rtsp=port_rtsp
        )
        if camera:
            # Sync camera from VMS, if camera already exists, update other_info, return camera.
            self.update_id_vms(camera=camera, other_info=new_request["other_info"])
            print(f"Camera already exists {camera}, {obj_in}")
            raise HTTPException(status_code=400, detail="Camera already exists")

        # Get info that not parse in normal request
        new_request["company"] = user.company
        if new_request.get("brand_camera_id"):
            new_request["brand_camera"] = brand_camera_services.get_brand_camera(
                id=new_request["brand_camera_id"]
            )
        else:
            new_request["brand_camera"] = brand_camera_services.get_by_key(key="OTHER")
        type_service_ids = new_request["type_service_ids"]

        # Create camera
        new_camera = super().create(obj_in=new_request)

        # Handle when camera is ai camera -> create mapping
        if new_request["is_ai"]:
            mapping_services.create_mapping_camera(
                camera=new_camera, type_service_ids=type_service_ids
            )

        return new_camera

    def update_camera(self, *, id: str, obj_in: CameraUpdate) -> Camera:
        # print("Update camera", id, obj_in)
        update_data = super().clean_update_input(obj_in)
        # print("Update data", update_data)
        be_updated_camera = self.get_camera(id=id)

        # Get pair (ip_address, port_rtsp) from update_data
        if update_data.get("rtsp"):
            ud_port_rtsp = self.get_port_rtsp(update_data["rtsp"])
        else:
            ud_port_rtsp = getattr(be_updated_camera, "port_rtsp", None)
        if update_data.get("ip_address"):
            ud_ip_address = update_data["ip_address"]
        else:
            ud_ip_address = be_updated_camera.ip_address

        # Check if camera already exists: ip_address, port rtsp
        self.check_unique_camera(
            camera_id=id, ip_address=ud_ip_address, port_rtsp=ud_port_rtsp
        )

        # Brand
        if update_data.get("brand_camera_id"):
            brand_id = update_data["brand_camera_id"]
            brand = brand_camera_services.get_brand_camera(id=brand_id)
            update_data["brand_camera"] = brand
            del update_data["brand_camera_id"]

        # Mapping
        if "is_ai" in update_data:
            if update_data["is_ai"] and "type_service_ids" in update_data:
                type_service_ids = update_data["type_service_ids"]
                mapping_services.update_mapping_camera(
                    camera=be_updated_camera, type_service_ids=type_service_ids
                )
                del update_data["type_service_ids"]
            else:
                mapping_services.remove_by_camera(camera_id=str(be_updated_camera.id))
                if "type_service_ids" in update_data:
                    del update_data["type_service_ids"]

        # Remove fields from update_data that have not changed
        for field in list(update_data.keys()):  # Create a copy of keys
            if getattr(be_updated_camera, field) == update_data[field]:
                del update_data[field]

        # If nothing has changed, return the original update_camera without updating
        if not update_data:
            return be_updated_camera

        return super().update(db_obj=be_updated_camera, obj_in=update_data)

    def remove_camera(self, *, id: str):
        """Remove camera by id. If camera has related process, raise error."""
        from app.services.process_services import process_services
        from app.services.event_services import event_services

        count_process_related = process_services.count_by_camera(camera_id=id)
        if count_process_related > 0:
            raise HTTPException(
                status_code=400,
                detail="Vui lòng xóa hết các tiến trình liên quan trước",
            )
        mapping_services.remove_by_camera(camera_id=id)
        event_services.remove_field_camera(camera_id=id)
        return super().remove(id=id)

    def get_by_brand_id(self, brand_id: str) -> list[Camera] | None:
        """Get all cameras by brand_id"""
        return list(self.engine.find(Camera, Camera.brand_camera == ObjectId(brand_id)))

    def remove_camera_brand(self, brand_id: str):
        """
        Remove brand of all cameras that have brand_id.
        Change to null brand.
        """

        cameras = self.get_by_brand_id(brand_id=brand_id)

        # Get null brand -> Change brand of all cameras that have brand deleted to null brand
        null_brand = brand_camera_services.get_by_key(key="OTHER")
        if null_brand is None:
            null_brand = brand_camera_services.create_brand_camera(
                obj_in={"name": "Khác", "key": "OTHER"}
            )

        for camera in cameras:
            self.update(db_obj=camera, obj_in={"brand_camera": null_brand})

    def sync_from_vms(self, user: User):
        """
        Sync cameras from VMS to database.
        1. Get VMS info of user
        2. Get cameras from VMS
        3. Compare with cameras in database
        4. Create new cameras
        5. Update cameras
        6. Return report
        """
        from app.services.vms_services import vms_services

        # from app.services.process_services import process_services
        from app.schemas.brand_camera_schemas import BrandCameraCreate
        from app.core.config import settings

        # from app.schemas.process_schemas import ProcessCreate
        from app.common.constants.enums import VmsTypeEnum
        from app.services.process_services import process_services

        # def camera_match(rtsp1: str, rtsp2: str) -> bool:
        #     """
        #     camera match if rtsp1 and rtsp2 have the same address and port
        #     """
        #     try:
        #         address1 = rtsp1.split(":")[1].replace("//", "")
        #         address2 = rtsp2.split(":")[1].replace("//", "")
        #     except Exception:
        #         return False
        #     if address1 == address2:
        #         port1 = rtsp1.split(":")[2].split("/")[0]
        #         port2 = rtsp2.split(":")[2].split("/")[0]
        #         return port1 == port2
        #     return False

        def get_camera_info_nx_server(data: dict):
            id_vms = data["id"][1:-1]

            camera = {
                "rtsp": data["parameters"]["streamUrls"]["1"]
                if "streamUrls" in data["parameters"]
                else "",
                "username": data["credentials"]["user"]
                if "user" in data["credentials"]
                else "",
                "password": data["credentials"]["password"]
                if "user" in data["credentials"]
                else "",
                "name": data["name"],
                "other_info": {
                    "id_vms": id_vms,
                },
            }
            return camera

        def get_camera_info_oryza_server(data: dict):
            id_vms = data.get("id", "")
            if len(id_vms) >= 2:
                id_vms = id_vms[1:-1]
            credentials: dict = data.get("credentials", {})
            camera = {
                "other_info": {
                    "id_vms": id_vms,
                },
                "rtsp": data.get("parameters").get("streamUrls").get("1", ""),
                "name": data.get("name", ""),
                "username": credentials.get("user", ""),
                "password": credentials.get("password", ""),
            }
            return camera

        vms_info = vms_services.get_my_company_vms(user=user)
        if not vms_info:
            raise HTTPException(status_code=400, detail="VMS not found")
        vms_url = vms_info.ip_address + ":" + str(vms_info.port)

        auth_header = vms_services.get_auth_header(vms_info)
        try:
            data_camera = vms_services.request_api(
                vms_url,
                "/rest/v2/devices",
                "GET",
                headers=auth_header,
                verify=False,
                timeout=settings.REQUEST_TIMEOUT,
            )
        except TimeoutError:
            raise HTTPException(status_code=400, detail="Timeout error")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        with open("temp/sync_data_camera.json", "w") as f:
            json.dump(data_camera, f, indent=4)

        vms_sync_report = {
            "total": len(data_camera),
        }
        create_count = 0
        update_count = 0
        errors = []
        creates = []
        cameras = self.get_cameras(user=user)

        for data in data_camera:
            ip_address = data["url"].split(":")[1].replace("//", "")
            try:
                port = int(data["url"].split(":")[2].split("/")[0])
            except Exception:
                port = 0

            if port == 0:
                ip_address = ip_address.split("/")[0]
                port = 80

            null_brand = brand_camera_services.get_by_name(name="Khác")
            if not null_brand:
                null_brand = brand_camera_services.create_brand_camera(
                    obj_in=BrandCameraCreate(name="Khác", key="OTHER")
                )
            if "vendor" not in data:
                brand_id = str(null_brand.id)
            else:
                brand_id = brand_camera_services.get_id_by_name(name=data["vendor"])
                if not brand_id:
                    brand_id = str(null_brand.id)

            if vms_info.vms_type == VmsTypeEnum.nx:
                camera = get_camera_info_nx_server(data)
            elif vms_info.vms_type == VmsTypeEnum.oryza:
                camera = get_camera_info_oryza_server(data)
            else:
                return

            id_vms = camera["other_info"]["id_vms"]
            vms_address = vms_info.ip_address.replace("https", "rtsp").replace(
                "http", "rtsp"
            )
            camera = {
                **camera,
                "company": str(user.company.id),
                "ip_address": ip_address,
                "port": int(port),
                "is_ai": False,
                "brand_camera_id": brand_id,
                "type_service_ids": [],
                "vms_type": vms_info.vms_type,
                "rtsp_vms": f"{vms_address}:{settings.VMS_RTSP_PORT}/{id_vms}_0",
            }

            update_fields = [
                "company",
                "other_info",
                "rtsp",
                "rtsp_vms",
                "name",
                "username",
                "vms_type",
            ]
            # Use dictionary comprehension to create update_data with only the specified fields
            update_data = {field: camera[field] for field in update_fields}
            print("Update data when sync vms", update_data)
            updated = False
            for current_camera in cameras:
                # if camera_match(camera["old_rtsp"], current_camera.rtsp):
                if (current_camera.ip_address == camera["ip_address"]) and (
                    current_camera.port == camera["port"]
                ):
                    self.update_camera(
                        user=user,
                        id=str(current_camera.id),
                        obj_in=CameraUpdate(**update_data),
                    )
                    updated = True
                    update_count += 1
                    break
            if not updated:
                try:
                    new_camera = self.create_camera(
                        user=user, obj_in=CameraCreate(**camera)
                    )
                    create_count += 1
                    creates.append(new_camera)
                except Exception as e:
                    print("Error creating camera when sync from vms", e)
                    pass
        # Remove camera that not appear in the new vms
        cameras = self.get_cameras(user=user)
        for current_camera in cameras:
            if (
                current_camera.vms_type != ""
                and current_camera.vms_type is not None
                and current_camera.vms_type != vms_info.vms_type
            ):
                print(f"Remove camera {current_camera} because vms type is different")
                camera_id = str(current_camera.id)
                processes = process_services.get_by_camera_id(camera_id=camera_id)
                print(f"Remove {len(list(processes))} process related to the camera")
                for process in processes:
                    try:
                        process_services.kill_process_raw(process=process)
                        self.engine.delete(process)
                    except Exception as e:
                        print("Error remove process", e)
                self.engine.delete(current_camera)
                print("Remove camera done")
        vms_sync_report["create"] = create_count
        vms_sync_report["create_details"] = creates
        vms_sync_report["update"] = update_count
        vms_sync_report["errors"] = len(errors)
        vms_sync_report["error_details"] = errors
        return vms_sync_report

    def generate_rtsp(self, rq: GenerateRTSP):
        from onvif import ONVIFCamera

        try:
            camera = ONVIFCamera(rq.address, rq.port, rq.username, rq.password)
            media_service = camera.create_media_service()
            profiles = media_service.GetProfiles()
            for profile in profiles:
                if profile.Name.lower().find("main") >= 0:
                    stream_setup = media_service.create_type("GetStreamUri")
                    stream_setup.ProfileToken = profile.token
                    stream_setup.StreamSetup = {
                        "Stream": "RTP-Unicast",
                        "Transport": {"Protocol": "RTSP"},
                    }
                    rtsp = media_service.GetStreamUri(stream_setup).Uri
                    return {"data": rtsp}
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error get rtsp from camera, {e}"
            )
        raise HTTPException(status_code=400, detail="Error get rtsp from camera")

    def get_rtsp_auth(self, camera: Camera):
        username = camera.username
        password = camera.password
        if password.count("*") >= 3:
            return None
        if username is not None and password is not None:
            name_pass = f"{username}:{password}@"
            rtsp = camera.rtsp
            if rtsp == "" or rtsp is None:
                return None
            if name_pass not in rtsp:
                rtsp = rtsp.replace("rtsp://", f"rtsp://{name_pass}")
            return rtsp
        return None

    def get_rtsp_vms_auth(self, camera: Camera):
        from app.services.vms_services import vms_services

        id_vms = camera.other_info.get("id_vms", "")
        if id_vms == "":
            print("Get rtsp vms fail, id_vms not found")
            return None
        vms = vms_services.get_by_company_id(company_id=str(camera.company.id))
        address = vms.ip_address.replace("http://", "").replace("https://", "")
        rtsp = f"rtsp://{vms.username}:{vms.password}@{address}:{vms.port}/{id_vms}"
        print(f"Get rtsp vms success, Generated RTSP URL: {rtsp}")
        return rtsp

    def get_list_rtsp(self, camera_id: str):
        import re

        camera = self.get(camera_id)
        if camera is None:
            raise HTTPException(status_code=400, detail="Camera not found")

        rtsp_pattern = re.compile(r"^rtsp://[^:]+:[^@]+@.+$")

        list_rtsp = []
        if camera.rtsp is not None:
            if rtsp_pattern.match(camera.rtsp):
                list_rtsp.append(camera.rtsp)
            rtsp_camera_auth = self.get_rtsp_auth(camera)
            if rtsp_camera_auth is not None and rtsp_camera_auth not in list_rtsp:
                list_rtsp.append(rtsp_camera_auth)
        rtsp_vms_auth = self.get_rtsp_vms_auth(camera)
        if rtsp_vms_auth is not None and rtsp_vms_auth not in list_rtsp:
            list_rtsp.append(rtsp_vms_auth)
        return {"data": list_rtsp}

    def get_hls_stream(self, camera_id: str):
        from app.services.vms_services import vms_services
        from app.common.constants.enums import VmsTypeEnum
        from app.core.config import settings

        camera = self.get(camera_id)
        if camera is None:
            raise HTTPException(status_code=400, detail="Camera not found")
        id_vms = camera.other_info.get("id_vms", "")
        if id_vms == "":
            raise HTTPException(status_code=400, detail="id_vms not found")
        vms = vms_services.get_by_company_id(company_id=str(camera.company.id))
        if vms is None:
            raise HTTPException(status_code=400, detail="VMS not found")
        protocol = vms.ip_address.split(":")[0]
        ip_address = vms.ip_address.split(":")[1].replace("//", "")
        if vms.vms_type == VmsTypeEnum.nx:
            url = f"{protocol}://{vms.username}:{vms.password}@{ip_address}:{settings.HLS_STREAM_PORT}/{id_vms}.m3u8"
        elif vms.vms_type == VmsTypeEnum.oryza:
            url = f"{vms.ip_address}:{settings.HLS_STREAM_PORT}/{id_vms}_0/index.m3u8"
        else:
            url = ""
        return {"data": url}

    def get_by_geo_unit(self, geo_unit_id: str):
        from app.services import geo_unit_services

        list_camera = []
        list_ward_id = geo_unit_services.get_list_ward_id(geo_unit_id)
        # print(len(list_ward_id))
        for ward_id in list_ward_id:
            cameras = self.engine.find(Camera, Camera.ward_id == ward_id)
            list_camera += list(cameras)
        return list_camera

    def get_video_record(self, camera_id: str, start_time: int, duration: int):
        from app.services.vms_services import vms_services

        camera = self.get(camera_id)
        if camera is None:
            raise HTTPException(status_code=404, detail="Camera not found")
        camera_id_vms = camera.other_info.get("id_vms")
        if not camera_id_vms:
            raise HTTPException(status_code=404, detail="Camera id_vms not found")
        vms = vms_services.get_by_company_id(company_id=str(camera.company.id))
        ip_address = vms.ip_address.split("//")[1]
        ip_address = f"https://{vms.username}:{vms.password}@{ip_address}"
        url = f"{ip_address}:{vms.port}/media/{camera_id_vms}.webm?pos={start_time}&duration={duration}"
        return {"data": url}


camera_services = CRUDCamera(Camera)
