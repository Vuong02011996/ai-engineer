from app.common.constants.rabbitmq_constants import FACE_RECOGNITION_EXCHANGES
from app.core.config import settings
from app.models import User
from app.services.base_services import CRUDBase

from app.models.camera_type_ai_mapping_model import CameraTypeAIMapping

from app.models.camera_model import Camera
from app.schemas.camera_type_ai_mapping_schemas import (
    CameraTypeAIMappingCreate,
    CameraTypeAIMappingUpdate,
)
from odmantic import ObjectId

from app.services.event_services import type_service_services


class CRUDCameraTypeAIMapping(
    CRUDBase[CameraTypeAIMapping, CameraTypeAIMappingCreate, CameraTypeAIMappingUpdate]
):
    def get_mapping(self, *, id: str):
        mapping = super().get(id)
        if not mapping:
            return None
        return mapping

    def get_camera_face(self, *, user: User):
        type_service_face = type_service_services.get_type_service_by_key(key=FACE_RECOGNITION_EXCHANGES)
        data = self.engine.find(
            CameraTypeAIMapping,
            {"type_service": type_service_face.id},

            sort=CameraTypeAIMapping.created.desc(),
        )
        return list(data)

    def get_mappings(self, *, page: int = 0, page_break: bool = False):
        return {"data": super().get_multi(page=page, page_break=page_break)}

    def get_mappings_by_camera(self, *, camera_id: str):
        """Get all ids of mappings by camera_id"""
        return list(
            self.engine.find(
                CameraTypeAIMapping, CameraTypeAIMapping.camera == ObjectId(camera_id)
            )
        )

    def create_mapping(self, *, obj_in: CameraTypeAIMappingCreate):
        """Create a new mapping"""
        return super().create(obj_in=obj_in)

    def create_mapping_camera(self, *, camera: Camera, type_service_ids: dict):
        """Create mappings for a camera, input camera object and list type_service_ids"""
        from app.services.type_service_services import type_service_services

        # get list type service object
        type_service_ids = list(set(type_service_ids))
        type_services = []
        for type_service_id in type_service_ids:
            type_service = type_service_services.get(id=type_service_id)
            if type_service:
                type_services.append(type_service)

        # Create mappings
        for type_service in type_services:
            mapping_in = CameraTypeAIMappingCreate(
                camera=camera,
                type_service=type_service,
            )
            self.create_mapping(obj_in=mapping_in)

    def update_mapping_camera(self, *, camera: Camera, type_service_ids: dict):
        """Remove all existing mappings of a camera and create new mappings"""
        # Remove all existing mappings of a camera
        self.remove_by_camera(camera_id=str(camera.id))
        # Create new mappings
        self.create_mapping_camera(camera=camera, type_service_ids=type_service_ids)

    def remove_mapping(self, *, id: str):
        return super().remove(id=id)

    def remove_by_camera(self, *, camera_id: str):
        """Remove all mappings of a camera"""
        return self.engine.remove(self.model, self.model.camera == ObjectId(camera_id))

    def remove_by_type_service(self, *, type_service_id: str):
        """Remove all mapping of a type service"""
        return self.engine.remove(
            self.model, self.model.type_service == ObjectId(type_service_id)
        )


camera_type_ai_mapping_services = CRUDCameraTypeAIMapping(CameraTypeAIMapping)



