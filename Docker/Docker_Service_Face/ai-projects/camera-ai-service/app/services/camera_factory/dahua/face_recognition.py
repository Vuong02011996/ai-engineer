import uuid

import requests
from fastapi import HTTPException

from app.common.enum import TypeCameraEnum
from app.common.convert_image import convert_image
from app.models import Person
from app.models.person_camera_model import PersonCamera
from app.models.person_image import PersonImage
from app.schemas.base_face_camera_dahua import BaseCameraDahua
from app.schemas.face_group_dahua_schema import CreateFaceGroup
from app.schemas.person_camera_schemas import (
    PersonCameraCreateDTO,
    PersonCameraCreate,
    PersonCameraDelete,
    PersonCameraUpdate,
)
from app.schemas.person_dahua_schema import CreatePerson, DeletePerson, UpdatePerson
from app.schemas.person_image_schemas import PersonImageUpdateAuto
from app.services.camera_factory.camera import ICamera
from app.services.face_group_dahua_service import face_group_dahua_service
from app.services.person_camera_services import person_camera_services
from app.services.person_dahua_service import person_dahua_service


class Dahua(ICamera):
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
                    response = requests.get(item.url)
                    image_bytes = response.content
                    image_bytes = convert_image(image_bytes)
                    data = {
                        "host": camera.host_camera,
                        "username": camera.username_camera,
                        "password": camera.password_camera,
                        "uid": person_camera.person_id_camera,
                        "image": image_bytes,
                    }
                    person_dahua_service.update_person(update_data=UpdatePerson(**data))
                    data_update = {"image_id": str(item.id)}
                    person_camera_services.update(
                        db_obj=person_camera, obj_in=PersonCameraUpdate(**data_update)
                    )
                    return item
            except Exception:
                return None

    def create_person(
        self, res: PersonCameraCreateDTO, list_image: list[PersonImage], person: Person
    ):
        try:
            data_person = {
                "host": res.host_camera,
                "username": res.username_camera,
                "password": res.password_camera,
            }
            groups = face_group_dahua_service.get_all(
                data=BaseCameraDahua(**data_person)
            )
            try:
                group_ids = [group["groupID"] for group in groups["GroupList"].values()]
            except Exception:
                group_ids = []
            id_group = None
            if len(group_ids) == 0:
                face_group = {
                    "host": res.host_camera,
                    "username": res.username_camera,
                    "password": res.password_camera,
                    "group_name": uuid.uuid4().hex,
                    "group_detail": "",
                }
                data = face_group_dahua_service.create_face_group(
                    CreateFaceGroup(**face_group)
                )
                arr = data.split("=")
                if len(arr) == 2:
                    id_group = arr[1].strip()
            else:
                id_group = group_ids[0].strip()
            # id_group = "47"
            # print("id_group", id_group)
            for item in list_image:
                try:
                    urlImage = item.url
                    response = requests.get(urlImage)
                    image_bytes = response.content
                    image_bytes = convert_image(image_bytes)
                    if not image_bytes:
                        continue

                    data = {
                        "host": res.host_camera,
                        "username": res.username_camera,
                        "password": res.password_camera,
                        "group_id": id_group,
                        "name": person.name,
                        "image": image_bytes,
                    }
                    # print("data", data)
                    data_create = person_dahua_service.create_preson(
                        CreatePerson(**data)
                    )
                    # print("-------xuong---------------")
                    array_data = data_create.split("=")
                    if len(array_data) == 2:
                        id_user = array_data[1].strip()
                        data_save = {
                            "person_id": res.person_id,
                            "camera_id": res.id_camera,
                            "person_id_camera": id_user,
                            "image_id": str(item.id),
                            "type_camera": TypeCameraEnum.dahua,
                            "other_info": {"group_id": id_group.strip()},
                        }
                        data_result = person_camera_services.create(
                            obj_in=PersonCameraCreate(**data_save)
                        )
                        return data_result
                except Exception as e:
                    print("Error create user camera", e)
                    continue

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating person {e}")

    def delete_person(
        self, id: str, res: PersonCameraDelete, person_camera: PersonCamera
    ):
        try:
            data_delete = {
                "host": res.host_camera,
                "username": res.username_camera,
                "password": res.password_camera,
                "group_id": person_camera.other_info["group_id"],
                "uid": person_camera.person_id_camera,
            }
            person_dahua_service.delete_person(DeletePerson(**data_delete))
        except Exception:
            pass
        person_camera_services.remove(id=id)
        return person_camera

    def update_person(self):
        print("Update camera Dahua")
