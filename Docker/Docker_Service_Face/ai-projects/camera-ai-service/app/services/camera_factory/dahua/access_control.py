import requests

from app.core.config import settings
from app.common.enum import TypeCameraEnum
from app.common.convert_image import convert_image

from app.models import Person
from app.models.person_image import PersonImage
from app.models.person_camera_model import PersonCamera

from app.schemas.person_camera_schemas import PersonCameraCreateDTO
from app.schemas.person_image_schemas import PersonImageUpdateAuto
from app.schemas.person_access_control_schemas import (
    CreatePersonCameraAccessControl as CreatePerson,
    UpdateImagePersonCameraAccessControl as UpdateImage,
    DeletePersonCameraAccessControl as DeletePerson,
)
from app.schemas.person_camera_schemas import (
    PersonCameraDelete,
    PersonCameraCreate,
    PersonCameraUpdate,
)
from app.services.camera_factory.camera import ICamera
from app.services.person_access_control_services import (
    person_access_control_services as person_ac_services,
)
from app.services.person_camera_services import person_camera_services


class AccessControl(ICamera):
    def create_person(
        self, res: PersonCameraCreateDTO, list_image: list[PersonImage], person: Person
    ):
        print("Create person access control", res, list_image, person)
        for item in list_image:
            try:
                image = requests.get(item.url, timeout=settings.REQUEST_TIMEOUT).content

                # Create person in camera
                data_create = CreatePerson(
                    address=res.host_camera,
                    port=res.port_camera,
                    username=res.username_camera,
                    password=res.password_camera,
                    pid=str(person.id),
                    person_name=person.name,
                    image=image,
                )
                recno, user_id = person_ac_services.create_person(data_create)
                if recno is not None:
                    print("Person created in access control camera")
                else:
                    return None

                # Save person camera to database
                data_save = {
                    "person_id": res.person_id,
                    "camera_id": res.id_camera,
                    "person_id_camera": user_id,
                    "image_id": str(list_image[0].id),
                    "type_camera": TypeCameraEnum.access_control,
                    "other_info": {
                        "user_id": recno,
                    },
                }

                # Return data
                data_result = person_camera_services.create(
                    obj_in=PersonCameraCreate(**data_save)
                )
                return data_result
            except Exception as e:
                print("Error creating person access control", e)
                continue
        return None

    def update_person():
        pass

    def delete_person(
        self, id: str, res: PersonCameraDelete, person_camera: PersonCamera
    ):
        person_ac_services.delete_person(
            rq=DeletePerson(
                address=res.host_camera,
                port=res.port_camera,
                username=res.username_camera,
                password=res.password_camera,
                recno=person_camera.other_info["user_id"],
            )
        )
        person_camera_services.remove(id=id)
        return person_camera

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
                    response = requests.get(item.url, timeout=settings.REQUEST_TIMEOUT)
                    image_bytes = response.content

                    image_bytes = convert_image(image_bytes)

                    data_update_cam = {
                        "address": camera.host_camera,
                        "port": camera.port_camera,
                        "username": camera.username_camera,
                        "password": camera.password_camera,
                        "user_id": person_camera.person_id_camera,
                        "image": image_bytes,
                    }
                    person_ac_services.update_image_person(
                        rq=UpdateImage(**data_update_cam)
                    )

                    data_update_db = {
                        "image_id": str(item.id),
                        "person_id_camera": person_camera.person_id_camera,
                    }
                    print("data update", data_update_db)
                    person_camera_services.update(
                        db_obj=person_camera,
                        obj_in=PersonCameraUpdate(**data_update_db),
                    )
                    return item
            except Exception as e:
                print("Error create user camera", e)
                continue
