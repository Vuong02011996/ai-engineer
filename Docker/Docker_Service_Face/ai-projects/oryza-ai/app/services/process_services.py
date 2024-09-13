import asyncio
from fastapi import HTTPException
import requests

from odmantic import ObjectId
from odmantic.exceptions import DocumentParsingError

from app.common.utils.payload_process import get_payload
from app.core.config import settings

from app.services.base_services import CRUDBase
from app.services.camera_services import CRUDCamera
from app.services.service_services import CRUDService, type_service_services

from app.models.service_model import Service
from app.models.process_model import Process
from app.models.user_model import User
from app.models.camera_model import Camera
from app.models.server_model import Server

from app.schemas.process_schemas import ProcessCreate, ProcessUpdate, ProcessRun

from app.common.constants.enums import ProcessStatus, TypeServiceEnum
from app.websocket.web_socket_super_admin import web_socket_super_admin

camera_services = CRUDCamera(Camera)
service_services = CRUDService(Service)


class CRUDProcess(CRUDBase[Process, ProcessCreate, ProcessUpdate]):
    def check_user_permission(self, user: User, camera: Camera):
        if user.is_superuser:
            return
        if str(camera.company.id) != str(user.company.id):
            raise HTTPException(status_code=403, detail="Not enough permissions")

    def get_process_start_by_service_id(self, service_id: str):
        process = self.engine.find(
            Process,
            Process.service == ObjectId(service_id),
            Process.status == ProcessStatus.start,
        )
        return list(process)

    def get_process(self, *, user: User, id: str) -> Process:
        try:
            process = super().get(id=id)
        except DocumentParsingError as e:
            raise HTTPException(status_code=400, detail=f"Error getting process, {e}")
        if not process:
            raise HTTPException(status_code=404, detail="Process not found")

        self.check_user_permission(user, process.camera)
        return process

    def update_status_by_service_id(self, service_id: str, status: ProcessStatus):
        processes = self.engine.find(Process, {"service": ObjectId(service_id)})
        for process in processes:
            try:
                process.status = status
                self.engine.save(process)
            except Exception as e:
                print(f"Error updating process status, {e}")
        return processes

    def update_status_by_id(self, id: str, status: ProcessStatus):
        process = super().get(id=id)
        process.status = status
        asyncio.run(
            web_socket_super_admin.send_company_message_json(
                {
                    "type": "STATUS_PROCESS",
                    "data": {"id": str(process.id), "status": status},
                }
            )
        )
        return self.engine.save(process)

    def run_process(self, *, obj_in: ProcessRun, is_router: bool = True):
        process = super().get(id=obj_in.process_id)
        # self.check_user_permission(user=user, camera=camera)
        service: Service = process.service
        server: Server = service.server

        total_process = self.get_process_start_by_service_id(service_id=str(service.id))
        if len(total_process) >= service.max_process:
            raise HTTPException(status_code=400, detail="Max process reached")

        url = f"http://{server.ip_address}:{service.port}/enable"
        payload = get_payload(process)
        if not payload:
            raise HTTPException(status_code=400, detail="Error getting payload")
        payload["is_debug"] = obj_in.is_debug

        # Log when call to sub-server to run process
        info = {
            "server": server.ip_address,
            "port": service.port,
            "process_id": str(process.id),
            "service": service.name,
            "payload": payload,
        }
        print(f"\nRunning process: {info}")
        if is_router:
            process.isEnable = True
            process.is_debug = obj_in.is_debug
            self.engine.save(process)
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 201 or response.status_code == 200:
                process.status = ProcessStatus.start

            else:
                raise HTTPException(
                    status_code=400,
                    detail="Error running process: call to sub-server failed",
                )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error running process, {e}")
        return True

    def kill_process(self, *, user: User, process_id: str, is_router: bool = True):
        process: Process = self.get_process(user=user, id=process_id)
        camera: Camera = process.camera
        self.check_user_permission(user=user, camera=camera)
        service: Service = process.service
        server: Server = service.server
        url = f"http://{server.ip_address}:{service.port}/kill"
        if is_router:
            process.isEnable = False
            process.is_debug = False
            self.engine.save(process)
        try:
            # background_tasks.add_task(write_notification, email, message="some notification")
            response = requests.post(url, json={"process_id": process_id}, timeout=5)
            print(response.content)
            if response.status_code == 201 or response.status_code == 200:
                process.status = ProcessStatus.stop

            else:
                raise HTTPException(
                    status_code=400,
                    detail="Error killing process: call to sub-server failed",
                )
        except Exception as e:
            print("----------------------------------------------------")
            raise HTTPException(status_code=400, detail=f"Error killing process, {e}")

        return True

    def create_process(self, *, user: User, obj_in: ProcessCreate) -> Process:
        # Check if the camera exist and the user has permission
        camera = camera_services.get_camera(id=obj_in.camera_id)
        self.check_user_permission(user, camera=camera)
        # Check if the service exist
        service = service_services.get_service(id=obj_in.service_id)

        process_exist = self.engine.find_one(
            Process,
            Process.camera == ObjectId(obj_in.camera_id),
            Process.service == ObjectId(obj_in.service_id),
        )

        if process_exist:
            raise HTTPException(status_code=400, detail="Process already exists")

        new_obj_in = obj_in.model_dump()
        new_obj_in["camera"] = camera
        new_obj_in["service"] = service
        del new_obj_in["camera_id"]
        del new_obj_in["service_id"]
        if service.type == TypeServiceEnum.ai_camera:
            from app.services.service_services import type_service_services

            type_service = type_service_services.get_type_service(
                id=obj_in.id_type_service
            )
            new_obj_in["id_type_service"] = str(type_service.id)
        else:
            new_obj_in["id_type_service"] = str(service.type_service.id)

        try:
            new_obj_in["company"] = user.company
            process = super().create(obj_in=new_obj_in)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating process, {e}")
        return process

    def get_processes(
        self, *, page: int = 0, page_break: bool = False, user: User
    ) -> list[Process]:
        processes = super().get_multi(page=page, page_break=page_break)
        if user.is_superuser:
            return processes
        result = []
        for process in processes:
            camera: Camera = camera_services.get_camera(id=str(process.camera.id))
            if camera and camera.company.id == user.company.id:
                result.append(process)
        return result

    def get_by_id_type_service(
        self,
        *,
        id_type_service=str,
        data_search=None,
        page: int = 0,
        page_break: bool = False,
        user: User,
    ):
        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )
        cursor = self.engine.find(
            Process,
            Process.id_type_service == id_type_service,
            Process.company == user.company.id,
            **offset,
            sort=self.model.created.desc(),
        )
        return list(cursor)

    def get_count_by_id_type_service(
        self,
        *,
        id_type_service=str,
        data_search=None,
        user: User,
    ):
        cursor = self.engine.count(
            Process,
            Process.id_type_service == id_type_service,
            Process.company == user.company.id,
        )
        return cursor

    def get_processes_by_camera_id(
        self, *, camera_id: str, user: User, page: int = 0, page_break: bool = False
    ) -> list[Process]:
        camera = camera_services.get_camera(id=camera_id)
        self.check_user_permission(user=user, camera=camera)
        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )
        processes = self.engine.find(
            Process,
            Process.camera == ObjectId(camera_id),
            **offset,
            sort=Process.created.desc(),
        )
        for process in processes:
            try:
                service = type_service_services.get_type_service_by_id(
                    process.id_type_service
                )
                process.service.type_service = service
            except Exception:
                continue
        return list(processes)

    def get_by_camera_id(self, *, camera_id: str):
        return self.engine.find(Process, Process.camera == ObjectId(camera_id))

    def get_by_camera_and_type_service(self, *, camera_id: str, type_service_id: str):
        return self.engine.find_one(
            Process,
            Process.camera == ObjectId(camera_id),
            Process.id_type_service == type_service_id,
        )

    def update_process(self, *, id: str, obj_in: ProcessUpdate, user: User) -> Process:
        from app.services.server_services import server_services

        process = super().get(id=id)
        if not process:
            raise HTTPException(status_code=404, detail="Process not found")

        self.check_user_permission(user=user, camera=process.camera)
        # Check if the server exist
        if obj_in.service_id:
            server: Server = server_services.get_server(id=obj_in.service_id)
            if not server:
                raise HTTPException(status_code=404, detail="Server not found")
            services = service_services.get_services_by_server_id(server_id=server.id)
            for service in services:
                if str(process.service.id) == str(service.id):
                    break
                raise HTTPException(
                    status_code=400, detail="Server is not compatible with the process"
                )
        # Update the process
        return super().update(db_obj=process, obj_in=obj_in)

    def remove_process(self, *, user: User, id: str) -> Process:
        process = self.get_process(user=user, id=id)
        self.kill_process_raw(process=process)
        return super().remove(id=id)

    def count_by_camera(self, *, camera_id: str):
        """Count process related to a camera"""
        return self.engine.count(self.model, self.model.camera == ObjectId(camera_id))

    def kill_process_raw(self, *, process: Process):
        """Just try to kill process, no matter the server online or offline(if server offline, process dead)"""
        # process: Process = self.get(id=process_id)
        service: Service = process.service
        server: Server = service.server
        url = f"http://{server.ip_address}:{service.port}/kill"
        try:
            requests.post(url, json={"process_id": str(process.id)}, timeout=5)
        except Exception:
            pass

    def get_by_service_id(self, *, service_id: str):
        """Get all Process by a service"""
        return list(self.engine.find(Process, Process.service == ObjectId(service_id)))

    def remove_by_service(self, *, service_id: str):
        """Remove all Process by a service"""
        processes = self.get_by_service_id(service_id=service_id)
        for process in processes:
            self.remove(id=str(process.id))

    def get_process_enable_by_service_id(self, service_id: str):
        process = self.engine.find(
            Process,
            {"service": ObjectId(service_id)},
            Process.isEnable == True,  # noqa
        )
        return list(process)

    def get_preview_image_by_process_id(self, process_id: str):
        import cv2
        import os
        from app.common.utils.minio_services import minio_services

        try:
            process = super().get(id=process_id)
            if not process:
                raise HTTPException(status_code=404, detail="Process not found")
            rtsp = process.rtsp
            print("Get preview image of process:", process_id, "rtsp:", rtsp)
            cap = cv2.VideoCapture(rtsp)
            if not cap.isOpened():
                raise HTTPException(status_code=400, detail="Camera not open")
            ret, frame = cap.read()
            if not ret:
                raise HTTPException(status_code=400, detail="Camera not open")
            cap.release()
            if not os.path.exists("./temp"):
                os.makedirs("./temp")
            name = f"{process_id}_{str(process.camera.id)}"
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


process_services = CRUDProcess(Process)
