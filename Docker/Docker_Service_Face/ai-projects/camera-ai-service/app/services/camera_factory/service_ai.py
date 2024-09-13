import requests
from fastapi import HTTPException

from app.common.enum import TypeCameraEnum

from app.models import Person
from app.models.person_camera_model import PersonCamera
from app.models.person_image import PersonImage

from app.schemas.person_camera_schemas import (
    PersonCameraCreateDTO,
    PersonCameraCreate,
    PersonCameraDelete,
)
from app.schemas.person_image_schemas import PersonImageUpdateAuto

from app.services.camera_factory.camera import ICamera
from app.services.person_camera_services import person_camera_services


class ServiceAI(ICamera):
    def update_image_person(
        self,
        list_image: list[PersonImage],
        id_image: str,
        camera: PersonImageUpdateAuto,
        person_camera: PersonCamera,
    ):
        list_url_image = []
        for item in list_image:
            list_url_image.append(item.url)
        data_send = {
            "user_id": str(person_camera.person_id_camera),
            "data": list_url_image,
        }
        try:
            ipaddress = camera.host_camera
            port = camera.port_camera
            url_send = f"http://{ipaddress}:{port}/api/identities/update"
            res_dt = requests.put(url_send, json=data_send)
            return res_dt.json()
        except Exception:
            return None

    def create_person(
        self, res: PersonCameraCreateDTO, list_image: list[PersonImage], person: Person
    ):
        try:
            list_url_image = []
            for item in list_image:
                list_url_image.append(item.url)
            data_send = {
                "name": person.name,
                "type": "Nhan vien",
                "data": list_url_image,
            }
            url_send = (
                f"http://{res.host_camera}:{res.port_camera}/api/identities/register"
            )
            res_dt = requests.post(url_send, json=data_send)
            if res_dt.status_code == 200:
                data = res_dt.json()
                data_save = {
                    "person_id": res.person_id,
                    "camera_id": res.id_camera,
                    "person_id_camera": data["user_id"],
                    "image_id": "",
                    "type_camera": TypeCameraEnum.face_service,
                    "other_info": {},
                    "group_id": "",
                }
                data_result = person_camera_services.create(
                    obj_in=PersonCameraCreate(**data_save)
                )
                return data_result
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating person {e}")

    def delete_person(
        self, id: str, res: PersonCameraDelete, person_camera: PersonCamera
    ):
        url_send = f"http://{res.host_camera}:{res.port_camera}/api/identities/user_id/{person_camera.person_id_camera}"
        person_camera_services.remove(id=id)
        try:
            requests.delete(url_send)
        except Exception:
            pass
        return person_camera

    def update_person(self):
        print("Update camera Dahua")
