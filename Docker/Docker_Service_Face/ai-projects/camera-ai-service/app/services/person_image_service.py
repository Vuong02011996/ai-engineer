import os
from datetime import datetime
from fastapi import HTTPException
from odmantic import ObjectId

from app.common.enum import TypeCameraEnum
from app.common.image_face import check_one_face
from app.core.config import settings
from app.models import Person
from app.models.person_camera_model import PersonCamera
from app.models.person_image import PersonImage
from app.schemas.person_image_schemas import (
    PersonImageCreate,
    PersonImageUpdate,
    PersonImageUpdateAuto,
)
from app.services.base_services import CRUDBase
from app.services.camera_factory.camera_factory import camera_factory
from app.services.minio_services import MinioServices


class CRUDPersonImage(CRUDBase[PersonImage, PersonImageCreate, PersonImageUpdate]):
    minio_services = MinioServices()

    def get_image_by_person_id(self, person_id: str):
        return list(self.engine.find(PersonImage, PersonImage.person_id == person_id))

    def update_image(self, id_image: str, res: PersonImageUpdateAuto):
        listImage = self.get_image_by_person_id(str(res.id_person))
        person_cameras = self.engine.find_one(
            PersonCamera, PersonCamera.id == ObjectId(res.id_person_camera)
        )
        return camera_factory.update_image_person_camera(
            type=res.key_camera,
            list_image=listImage,
            id_image=id_image,
            camera=res,
            person_camera=person_cameras,
        )

    async def create_image_by_person(self, id_person: str, file):
        # clone file
        try:
            id_person = ObjectId(id_person)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting person id, {e}")
        person = self.engine.find_one(Person, Person.id == id_person)
        if not person:
            raise HTTPException(status_code=400, detail="Person not found")

        tim_now = datetime.now().strftime("%Y%m%d%H%M%S%f")
        name = f"{id_person}_{tim_now}"
        crop_path = os.path.join("./temp", name + ".jpg")
        contents = await file.read()
        with open(crop_path, "wb") as f:
            f.write(contents)
        try:
            check_one_face(contents)
        except Exception as e:
            os.remove(crop_path)
            raise HTTPException(status_code=400, detail=f"Error check face, {e}")
        status = self.minio_services.upload_file(
            crop_path, name + ".jpg", bucket=settings.BUCKET_FACE
        )
        os.remove(crop_path)
        if status is False:
            raise HTTPException(
                status_code=400,
                detail={"code": "4537", "message": "Upload image failed"},
            )
        image_create = {
            "person_id": str(id_person),
            "url": status,
            "name": name + ".jpg",
        }
        d = PersonImageCreate(**image_create)
        data_result = self.create(obj_in=d)
        person_camera = self.engine.find_one(
            PersonCamera,
            PersonCamera.person_id == str(id_person),
            PersonCamera.type_camera == TypeCameraEnum.face_service,
        )
        if person_camera:
            return {
                "person_camera": {
                    "id_person_camera": str(person_camera.id),
                    "type": TypeCameraEnum.face_service,
                    "id_camera": str(person_camera.camera_id),
                },
                "data": data_result,
            }
        return {"person_camera": None, "data": data_result}

    async def delete_image(self, id_person: str, id_image: str):
        image = self.get(id=id_image)
        if not image:
            raise HTTPException(status_code=400, detail="Image not found")

        list_image = self.get_image_by_person_id(person_id=id_person)
        if len(list_image) <= 1:
            raise HTTPException(
                status_code=400, detail="Person must have at least one image"
            )

        person_cameras = self.engine.find(
            PersonCamera, PersonCamera.person_id == id_person
        )

        list_result = []
        for person_camera in person_cameras:
            if (
                person_camera.type_camera == TypeCameraEnum.face_service
                or person_camera.image_id == id_image
            ):
                list_result.append(
                    {
                        "id_camera": str(person_camera.camera_id),
                        "type": person_camera.type_camera,
                        "id_person_camera": str(person_camera.id),
                    }
                )

        self.remove(id=id_image)
        self.minio_services.delete_file(image.name, bucket=settings.BUCKET_FACE)
        return list_result

    def delete_by_person_id(self, id_person: str):
        list_image = self.get_image_by_person_id(person_id=id_person)
        for image in list_image:
            self.remove(id=image.id)
            self.minio_services.delete_file(image.name, bucket=settings.BUCKET_FACE)
        return list_image


person_image_services = CRUDPersonImage(PersonImage)
