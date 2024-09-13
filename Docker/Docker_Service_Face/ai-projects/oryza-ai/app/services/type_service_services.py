from fastapi import HTTPException

from app.core.config import settings
from app.models.type_service_model import TypeService
from app.schemas.type_service_schemas import (
    TypeServiceUpdate,
    TypeServiceCreate,
    TypeServiceBase,
)
from app.services.base_services import CRUDBase
from odmantic import query


class CRUDTypeService(CRUDBase[TypeServiceBase, TypeServiceCreate, TypeServiceUpdate]):
    def count_type_services(self, data_search: str = None) -> int:
        common_conditions = query.match(TypeService.key, {"$ne": "OTHER"})
        if data_search is None:
            return self.engine.count(TypeService, common_conditions)
        else:
            search_conditions = query.or_(
                TypeService.name.match(f".*{data_search}.*"),
                TypeService.key.match(f".*{data_search}.*"),
            )
            combined_conditions = query.and_(
                common_conditions,
                search_conditions,
            )
            return self.engine.count(TypeService, combined_conditions)

    def create_type_service(self, data: TypeServiceCreate) -> TypeService:
        type_service_exist = self.engine.find_one(
            TypeService, TypeService.name == data.name
        )
        if type_service_exist:
            raise HTTPException(status_code=400, detail="Name already used")

        type_service_exist2 = self.engine.find_one(
            TypeService, TypeService.key == data.key
        )
        if type_service_exist2:
            raise HTTPException(status_code=400, detail="Key already used")

        return super().create(obj_in=data)

    def update_type_service(self, id: str, data: TypeServiceUpdate):
        type_service = self.get_type_service(id=id)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.model_dump(exclude_unset=True)
        update_data = {k: v for k, v in update_data.items() if v is not None}
        if update_data.get("name"):
            type_service_exist = self.engine.find_one(
                TypeService,
                TypeService.name == update_data.get("name"),
                TypeService.id != type_service.id,
            )
            if type_service_exist:
                raise HTTPException(status_code=400, detail="Name already used")
        if update_data.get("key"):
            type_service_exist = self.engine.find_one(
                TypeService,
                TypeService.key == update_data.get("key"),
                TypeService.id != type_service.id,
            )
            if type_service_exist:
                raise HTTPException(status_code=400, detail="Key already used")
        return super().update(db_obj=type_service, obj_in=update_data)

    def get_type_service(self, id: str) -> TypeService:
        type_service = super().get(id=id)
        if not type_service:
            raise HTTPException(status_code=404, detail="Type service not found")
        return type_service

    def get_type_service_by_id(self, id: str):
        type_service = super().get(id=id)
        if not type_service:
            return None
        return type_service

    def get_by_key(self, key: str):
        type_service = self.engine.find_one(TypeService, TypeService.key == key)
        return type_service

    def get_type_service_by_key(self, key: str):
        type_service = self.engine.find_one(TypeService, TypeService.key == key)
        if not type_service:
            raise HTTPException(status_code=404, detail="Type service not found")
        return type_service

    def get_type_services(
        self, *, page: int = 0, page_break: bool = False, data_search: str = None
    ) -> list[TypeService]:
        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )
        common_conditions = query.match(TypeService.key, {"$ne": "OTHER"})
        if data_search is not None:
            search_conditions = query.or_(
                TypeService.name.match(f".*{data_search}.*"),
                TypeService.key.match(f".*{data_search}.*"),
            )
            cursor = self.engine.find(
                TypeService,
                query.and_(common_conditions, search_conditions),
                **offset,
                sort=TypeService.created.desc(),
            )
        else:
            cursor = self.engine.find(
                TypeService,
                common_conditions,
                **offset,
                sort=TypeService.created.desc(),
            )
        return list(cursor)

    def remove_type_service(self, id: str):
        from app.services.webhook_services import webhook_services
        from app.services.event_services import event_services
        from app.services.camera_type_ai_mapping_services import (
            camera_type_ai_mapping_services as mapping_services,
        )
        from app.services.service_services import service_services

        # no need to change anything, just remove all related data
        mapping_services.remove_by_type_service(type_service_id=id)

        # Create null type service (if not exist)
        # -> get id
        # -> replace all type service id by null type service id
        type_service_null = self.engine.find_one(
            TypeService, (TypeService.key == "OTHER" or TypeService.name == "Khác")
        )
        if type_service_null is None:
            type_service_null = self.create_type_service(
                TypeServiceCreate(name="Khác", key="OTHER")
            )
        webhook_services.remove_field_type_service(
            type_service_id=id, null_obj=type_service_null
        )
        event_services.remove_field_type_service(
            type_service_id=id, null_obj=type_service_null
        )
        service_services.remove_field_type_service(
            type_service_id=id, null_obj=type_service_null
        )
        return super().remove(id=id)


type_service_services = CRUDTypeService(TypeService)
