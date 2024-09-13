import requests

from app.common.enum import TypeCameraEnum
from app.common.convert_image import convert_image
from app.core.config import settings

from app.models import Person
from app.models.person_camera_model import PersonCamera
from app.models.person_image import PersonImage

from app.schemas.person_camera_schemas import (
    PersonCameraCreateDTO,
    PersonCameraDelete,
    PersonCameraCreate,
    PersonCameraUpdate,
)
from app.schemas.person_image_schemas import PersonImageUpdateAuto
from app.schemas.person_hik_schemas import (
    CreatePersonCameraHik as CreatePerson,
    UpdateImagePersonCameraHik as UpdateImage,
    DeletePersonCameraHik as DeletePerson,
)

from app.services.camera_factory.camera import ICamera
from app.services.person_camera_services import person_camera_services
from app.services.person_hik_service import person_hik_services


class Hikvision(ICamera):
    def update_image_person(
        self,
        list_image: list[PersonImage],
        id_image: str,
        camera: PersonImageUpdateAuto,
        person_camera: PersonCamera,
    ):
        for item in list_image:
            try:
                if str(item.id) != id_image:
                    try:
                        response = requests.get(
                            item.url, timeout=settings.REQUEST_TIMEOUT
                        )
                        image_bytes = response.content
                    except requests.exceptions.Timeout:
                        print("Timeout error")
                        return None
                    image_bytes = convert_image(image_bytes)

                    data_update_cam = {
                        "address": camera.host_camera,
                        "port": camera.port_camera,
                        "username": camera.username_camera,
                        "password": camera.password_camera,
                        "pid": person_camera.other_info["pid"],
                        "image": image_bytes,
                    }
                    try:
                        new_pid, custom_id = person_hik_services.update_image_person(
                            update_data=UpdateImage(**data_update_cam)
                        )
                    except Exception as e:
                        print(f"An error occurred: {e}")

                    data_update_db = {
                        "image_id": str(item.id),
                        "person_id_camera": custom_id,
                        "other_info": {
                            "pid": new_pid,
                        },
                    }
                    print("data update", data_update_db)
                    person_camera_services.update(
                        db_obj=person_camera,
                        obj_in=PersonCameraUpdate(**data_update_db),
                    )
                    return item
            except Exception:
                return None

    def create(
        self, res: PersonCameraCreateDTO, list_image: list[PersonImage], person: Person
    ):
        try:
            image = requests.get(
                list_image[0].url, timeout=settings.REQUEST_TIMEOUT
            ).content

            data_create = CreatePerson(
                username=res.username_camera,
                password=res.password_camera,
                address=res.host_camera,
                port=res.port_camera,
                name=person.name,
                image=convert_image(image, target_size=200),
            )
            pid, custom_pid = person_hik_services.create_person(data_create)

            data_save = {
                "person_id": res.person_id,
                "camera_id": res.id_camera,
                "person_id_camera": custom_pid,
                "image_id": str(list_image[0].id),
                "type_camera": TypeCameraEnum.hikvision,
                "other_info": {
                    "pid": pid,
                },
            }

            data_result = person_camera_services.create(
                obj_in=PersonCameraCreate(**data_save)
            )
            return data_result

        except requests.exceptions.Timeout:
            print("Timeout error")
            return None
        except Exception as e:
            print("Error creating person hik", e)
            return None

    def delete(self, id: str, res: PersonCameraDelete, person_camera: PersonCamera):
        person_hik_services.delete_person(
            data=DeletePerson(
                username=res.username_camera,
                password=res.password_camera,
                address=res.host_camera,
                port=res.port_camera,
                pid=person_camera.other_info["pid"],
            ),
        )
        person_camera_services.remove(id=id)
        return person_camera

    def update(self):
        print("Update camera hikvision")
