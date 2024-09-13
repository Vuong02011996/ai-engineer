from app.models import Person
from app.models.person_camera_model import PersonCamera
from app.models.person_image import PersonImage
from app.schemas.person_camera_schemas import PersonCameraCreateDTO, PersonCameraDelete
from app.schemas.person_image_schemas import PersonImageUpdateAuto


class ICamera:
    def create_person(
        self, res: PersonCameraCreateDTO, list_image: list[PersonImage], person: Person
    ):
        pass

    def delete_person(
        self, id: str, res: PersonCameraDelete, person_camera: PersonCamera
    ):
        pass

    def update_person(self):
        pass

    def update_image_person(
        self,
        list_image: list[PersonImage],
        id_image: str,
        camera: PersonImageUpdateAuto,
        person_camera: PersonCamera,
    ):
        pass
