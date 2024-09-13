from fastapi import HTTPException
from odmantic import ObjectId

from app.common.constants.enums import ProcessStatus
from app.core.config import settings
from app.models import Process
from app.models.service_model import Service
from app.schemas.service_schemas import ServiceBase, ServiceUpdate, ServiceCreate
from app.services.base_services import CRUDBase

from app.services.type_service_services import CRUDTypeService
from app.models.type_service_model import TypeService
from app.services.server_services import CRUDServer
from app.models.server_model import Server

type_service_services = CRUDTypeService(TypeService)
server_services = CRUDServer(Server)


class CRUDService(CRUDBase[ServiceBase, ServiceCreate, ServiceUpdate]):
    def count_service(self):
        return self.engine.count(Service)

    def get_service(self, id: str) -> Service:
        service = super().get(id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return service

    def get_service_by_id(self, id: str):
        service = super().get(id)
        if not service:
            return None
        return service

    def get_by_name(self, name: str):
        service = self.engine.find_one(Service, Service.name == name)
        if not service:
            return None
        return service

    def get_by_server_port(self, id_server: str, port: str):
        service = self.engine.find_one(
            Service, Service.server == ObjectId(id_server), Service.port == port
        )
        if not service:
            return None
        return service

    def get_services(self, *, page: int = 0, page_break: bool = False):
        return super().get_multi(page=page, page_break=page_break)

    def get_services_by_server_id(self, server_id: str):
        return self.engine.find(Service, str(Service.server.id) == server_id)

    def get_services_by_server_page(
        self,
        *,
        server_id: str,
        page_break,
        page: int = 0,
        data_search: str = None,
    ):
        try:
            server_id = ObjectId(server_id)
        except Exception:
            raise HTTPException(status_code=404, detail="Server not found")
        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )
        if data_search:
            cursor = self.engine.find(
                Service,
                {
                    "server": ObjectId(server_id),
                    "name": {"$regex": data_search, "$options": "i"},
                },
                **offset,
                sort=Service.created.desc(),
            )
        else:
            cursor = self.engine.find(
                Service,
                {"server": ObjectId(server_id)},
                **offset,
                sort=Service.created.desc(),
            )
        result = []
        for service in cursor:
            count_process = self.engine.count(
                Process,
                Process.service == service.id,
                Process.status == ProcessStatus.start,
            )
            data_service = {
                "id": str(service.id),
                "name": service.name,
                "port": service.port,
                "is_alive": service.is_alive,
                "max_process": service.max_process,
                "type_service": service.type_service,
                "server": service.server,
                "count_process": count_process,
                "created": service.created,
                "modified": service.modified,
                "type": service.type,
            }
            result.append(data_service)
        return result

    def get_count_services_by_server_page(
        self,
        *,
        server_id: str,
        data_search: str = None,
    ):
        try:
            server_id = ObjectId(server_id)
        except Exception:
            raise HTTPException(status_code=404, detail="Server not found")
        if data_search:
            cursor = self.engine.find(
                Service,
                {
                    "server": ObjectId(server_id),
                    "name": {"$regex": data_search, "$options": "i"},
                },
            )
        else:
            cursor = self.engine.find(Service, {"server": ObjectId(server_id)})
        return len(list(cursor))

    def create_service(self, request: ServiceCreate):
        from app.common.constants.rabbitmq_constants import loitering, intrusion

        type_service_exist = type_service_services.get_type_service(
            id=request.type_service_id
        )
        server = server_services.get_server(id=request.server_id)

        service_exist = self.get_by_name(name=request.name)
        if service_exist:
            raise HTTPException(status_code=400, detail="Name already used")

        service_exist2 = self.get_by_server_port(
            id_server=request.server_id, port=request.port
        )
        if service_exist2:
            # Check if both services have type_service.key of either loitering or intrusion
            if not (
                (
                    type_service_exist.key == loitering
                    and service_exist2.type_service.key == intrusion
                )
                or (
                    type_service_exist.key == intrusion
                    and service_exist2.type_service.key == loitering
                )
            ):
                raise HTTPException(status_code=400, detail="Port service already used")

        new_request = request.model_dump()
        new_request["server"] = server
        del new_request["server_id"]
        new_request["type_service"] = type_service_exist
        del new_request["type_service_id"]
        return super().create(obj_in=new_request)

    def update_service(self, id: str, data: ServiceUpdate):
        if data.type_service_id and not ObjectId.is_valid(data.type_service_id):
            raise HTTPException(status_code=404, detail="Type service not found")

        if data.server_id and not ObjectId.is_valid(data.server_id):
            raise HTTPException(status_code=404, detail="Server not found")

        if id and not ObjectId.is_valid(id):
            raise HTTPException(status_code=404, detail="Service not found")

        service: Service = super().get(id=ObjectId(id))
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.model_dump(exclude_unset=True)
        update_data = {
            k: v for k, v in update_data.items() if v is not None and v != ""
        }
        if update_data.get("name"):
            service_exist = self.engine.find_one(
                Service,
                Service.name == update_data.get("name"),
                Service.id != ObjectId(id),
            )
            if service_exist:
                raise HTTPException(
                    status_code=400, detail="Name service already exists"
                )
        if update_data.get("port"):
            service_exist = self.engine.find_one(
                Service,
                Service.port == update_data.get("port"),
                {"server": ObjectId(service.server.id)},
                Service.id != ObjectId(id),
            )
            if service_exist:
                raise HTTPException(
                    status_code=400, detail="Port service already exists"
                )

        if update_data.get("type_service_id"):
            type_service_exist = type_service_services.get(
                id=ObjectId(update_data.get("type_service_id"))
            )
            if not type_service_exist:
                raise HTTPException(status_code=404, detail="Type service not found")
            else:
                update_data["type_service"] = type_service_exist
                del update_data["type_service_id"]

        if update_data.get("server_id"):
            server_exist = server_services.get(id=update_data.get("server_id"))
            if not server_exist:
                raise HTTPException(status_code=404, detail="Server not found")
            else:
                update_data["server"] = server_exist
                del update_data["server_id"]
        return super().update(db_obj=service, obj_in=update_data)

    def update_status_by_ip_port(self, ip: str, port: str, status: bool):
        server = server_services.get_server_by_ip(ip)
        if not server:
            raise HTTPException(status_code=404, detail="Server not found")

        service = self.engine.find_one(
            Service, {"server": ObjectId(server.id)}, Service.port == str(port)
        )
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return super().update(db_obj=service, obj_in={"is_alive": status})

    def remove_service(self, *, id: str):
        from app.services.process_services import process_services

        process_services.remove_by_service(service_id=id)
        return super().remove(id=id)

    def remove_by_server(self, *, server_id: str):
        services = self.engine.find(Service, Service.server == ObjectId(server_id))
        for service in services:
            self.remove_service(id=str(service.id))

    def get_by_type_service(self, *, type_service_id: str):
        return list(
            self.engine.find(Service, Service.type_service == ObjectId(type_service_id))
        )

    def remove_field_type_service(self, *, type_service_id: str, null_obj: TypeService):
        services = self.get_by_type_service(type_service_id=type_service_id)
        for service in services:
            super().update(db_obj=service, obj_in={"type_service": null_obj})

    def get_info_by_key(self, key: str):
        type_service = self.engine.find_one(TypeService, TypeService.key == key)
        if not type_service:
            return None
        service = self.engine.find_one(
            Service, {"type_service": ObjectId(type_service.id)}
        )
        if not service:
            return None
        return service


service_services = CRUDService(Service)

# if __name__ == "__main__":
#     service_services.remove_field_type_service(type_service_id="6637441a4e09c9b80518fcca")
