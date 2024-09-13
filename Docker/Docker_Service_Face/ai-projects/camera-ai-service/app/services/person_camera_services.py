from fastapi import HTTPException

from app.common.check_sync_multi_camera import CheckSyncMultiCamera
from app.models.person_camera_model import PersonCamera
from app.schemas.person_camera_schemas import (
    PersonCameraCreate,
    PersonCameraUpdate,
    PersonCameraCreateDTO,
    PersonCameraDelete,
    PersonCameraCreateMultiCameraUser,
)
from app.services.base_services import CRUDBase


class CRUDPersonCamera(CRUDBase[PersonCamera, PersonCameraCreate, PersonCameraUpdate]):
    count = 0

    def create_user_camera(self, res: PersonCameraCreateDTO):
        from app.services.camera_factory.camera_factory import camera_factory
        from app.services.person_image_service import person_image_services
        from app.services.person_service import person_services

        person = person_services.get(id=res.person_id)
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
        exist_person_camera = self.engine.find_one(
            PersonCamera,
            PersonCamera.person_id == res.person_id,
            PersonCamera.camera_id == res.id_camera,
        )
        if exist_person_camera:
            raise HTTPException(status_code=400, detail="Person camera already exists")
        list_image = person_image_services.get_image_by_person_id(
            person_id=res.person_id
        )
        if len(list_image) == 0:
            raise HTTPException(status_code=404, detail="Person image not found")
        data = camera_factory.create_person_camera(
            type=res.key_camera, res=res, list_image=list_image, person=person
        )

        if data is None:
            raise HTTPException(status_code=400, detail="Type camera not support")
        return data

    def create_multi_user_camera(
        self, id_company, camera: PersonCameraCreateMultiCameraUser
    ):
        from app.services.person_service import person_services

        list_person = person_services.get_person_by_company(id_company)
        key_camera = camera.key_camera
        host_camera = camera.host_camera
        username_camera = camera.username_camera
        password_camera = camera.password_camera
        port_camera = str(camera.port_camera)
        list_success = []
        list_error = []
        count = 0
        for person in list_person:
            person_id = str(person["id"])
            count += 1
            # time.sleep(1)
            try:
                data = {
                    "person_id": person_id,
                    "id_camera": camera.id_camera,
                    "key_camera": key_camera,
                    "host_camera": host_camera,
                    "username_camera": username_camera,
                    "password_camera": password_camera,
                    "port_camera": port_camera,
                }
                self.create_user_camera(PersonCameraCreateDTO(**data))
                list_success.append(person_id)
            except Exception:
                list_error.append(person_id)
                continue
        checkSyncMultiCamera = CheckSyncMultiCamera()
        checkSyncMultiCamera.set_sync_multi_camera(camera.id_camera, False, "create")
        return {"success": list_success, "error": list_error}

    def delete_multi_user_camera(self, camera_id: str, res: PersonCameraDelete):
        list_person_camera = self.get_by_camera_id(camera_id)
        for person_camera in list_person_camera:
            try:
                # time.sleep(1)
                self.delete(str(person_camera.id), res, is_multi=True)
            except Exception:
                continue

        checkSyncMultiCamera = CheckSyncMultiCamera()
        checkSyncMultiCamera.set_sync_multi_camera(camera_id, False, "delete")

    """Thêm 1 user vào nhiều camera"""

    def create_multi_camera_user(
        self, person_id, cameras: list[PersonCameraCreateMultiCameraUser]
    ):
        list_success = []
        list_error = []
        count = 0
        for camera in cameras:
            camera_id = camera.id_camera
            count += 1
            try:
                data = {
                    "person_id": person_id,
                    "id_camera": camera_id,
                    "key_camera": camera.key_camera,
                    "host_camera": camera.host_camera,
                    "username_camera": camera.username_camera,
                    "password_camera": camera.password_camera,
                    "port_camera": str(camera.port_camera),
                }
                self.create_user_camera(PersonCameraCreateDTO(**data))
                list_success.append(camera_id)

            except Exception as e:
                print("Error create user camera", e)
                list_error.append(camera_id)
                continue
        return {"success": list_success, "error": list_error}

    def delete(self, id: str, res: PersonCameraDelete, is_multi=False):
        from app.services.camera_factory.camera_factory import camera_factory

        person_camera = self.get(id=id)

        if not person_camera:
            raise HTTPException(status_code=404, detail="Person camera not found")
        if not is_multi:
            checkSyncMultiCamera = CheckSyncMultiCamera()
            status = checkSyncMultiCamera.get_sync_multi_camera(person_camera.camera_id)
            if status and status["status"]:
                raise HTTPException(status_code=400, detail="Camera is being used")
        data = camera_factory.delete_person_camera(
            type=res.key_camera, id=id, res=res, person_camera=person_camera
        )
        if data is None:
            raise HTTPException(status_code=400, detail="Type camera not support")

        return data

    def get_by_person_id(self, person_id: str):
        return list(self.engine.find(PersonCamera, PersonCamera.person_id == person_id))

    def get_by_camera_id(self, camera_id: str):
        return list(self.engine.find(PersonCamera, PersonCamera.camera_id == camera_id))

    def get_by_person_id_camera(self, person_id_camera: str):
        return list(
            self.engine.find(
                PersonCamera, PersonCamera.person_id_camera == person_id_camera
            )
        )


person_camera_services = CRUDPersonCamera(PersonCamera)
