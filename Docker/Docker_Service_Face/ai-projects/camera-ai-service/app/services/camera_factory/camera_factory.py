from app.common.enum import TypeCameraEnum

from app.models import Person
from app.models.person_camera_model import PersonCamera
from app.models.person_image import PersonImage

from app.schemas.person_camera_schemas import PersonCameraCreateDTO, PersonCameraDelete
from app.schemas.person_image_schemas import PersonImageUpdateAuto

from app.services.camera_factory.camera import ICamera
from app.services.camera_factory.dahua.face_recognition import Dahua
from app.services.camera_factory.hikvision import Hikvision
from app.services.camera_factory.dahua.access_control import AccessControl
from app.services.camera_factory.dahua.traffic_intelligent import TrafficIntelligent
from app.services.camera_factory.service_ai import ServiceAI


class CameraFactory:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(CameraFactory, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.camera: dict[TypeCameraEnum, ICamera] = {}
        self.camera[TypeCameraEnum.dahua] = Dahua()
        self.camera[TypeCameraEnum.hikvision] = Hikvision()
        self.camera[TypeCameraEnum.access_control] = AccessControl()
        self.camera[TypeCameraEnum.kbvision] = TrafficIntelligent()
        self.camera[TypeCameraEnum.face_service] = ServiceAI()

    def register_camera(self, type: TypeCameraEnum, camera: ICamera):
        self.camera[type] = camera

    def create_person_camera(
        self,
        type: TypeCameraEnum,
        res: PersonCameraCreateDTO,
        list_image: list[PersonImage],
        person: Person,
    ):
        camera = self.camera[type]
        if camera is None:
            return None
        return camera.create_person(res=res, list_image=list_image, person=person)

    def delete_person_camera(
        self,
        type: TypeCameraEnum,
        id: str,
        res: PersonCameraDelete,
        person_camera: PersonCamera,
    ):
        camera = self.camera[type]
        if camera is None:
            return None
        return camera.delete_person(id=id, res=res, person_camera=person_camera)

    def update_person_camera(self, type: TypeCameraEnum, camera: ICamera):
        self.camera[type] = camera
        if camera is None:
            return None
        return camera.update_person()

    def update_image_person_camera(
        self,
        type: TypeCameraEnum,
        list_image: list[PersonImage],
        id_image: str,
        camera: PersonImageUpdateAuto,
        person_camera: PersonCamera,
    ):
        service = self.camera[type]
        if service is None:
            return None
        return service.update_image_person(
            list_image=list_image,
            id_image=id_image,
            camera=camera,
            person_camera=person_camera,
        )


camera_factory = CameraFactory()
