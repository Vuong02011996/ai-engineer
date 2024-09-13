from fastapi import HTTPException

from app.models import Service
from app.models.server_model import Server
from app.schemas.server_schemas import ServerBase, ServerCreate, ServerUpdate
from app.services.base_services import CRUDBase


class CRUDServer(CRUDBase[ServerBase, ServerCreate, ServerUpdate]):
    def count_server(self) -> int:
        return self.engine.count(Server)

    def create_server(self, data: ServerCreate):
        server_exist = self.engine.find_one(Server, Server.name == data.name)
        if server_exist:
            raise HTTPException(status_code=400, detail="Name already used")

        server_exist2 = self.engine.find_one(
            Server, Server.ip_address == data.ip_address
        )
        if server_exist2:
            raise HTTPException(status_code=400, detail="IP address already used")

        return super().create(obj_in=data)

    def update_server(self, id: str, data: ServerUpdate):
        server: Server = self.get_server(id=id)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.model_dump(exclude_unset=True)
        update_data = {k: v for k, v in update_data.items() if v is not None}
        if update_data.get("name"):
            server_exist = self.engine.find_one(
                Server,
                Server.name == update_data.get("name"),
                Server.id != server.id,
            )
            if server_exist:
                raise HTTPException(status_code=400, detail="Name already used")
        if update_data.get("ip_address"):
            server_exist2 = self.engine.find_one(
                Server,
                Server.ip_address == update_data.get("ip_address"),
                Server.id != server.id,
            )
            if server_exist2:
                raise HTTPException(status_code=400, detail="IP address already used")
        return super().update(db_obj=server, obj_in=update_data)

    def get_server(self, id: str):
        type_service = super().get(id=id)
        if not type_service:
            raise HTTPException(status_code=404, detail="Server not found")
        return type_service

    def get_server_by_ip(self, ip: str):
        server = self.engine.find_one(Server, Server.ip_address == ip)
        if not server:
            return None
        return server

    def get_servers(self, *, page: int = 0, page_break: bool = False):
        datas: list[Server] = super().get_multi(page=page, page_break=page_break)
        result = []
        for data in datas:
            count = self.engine.count(Service, {"server": data.id})
            result.append(
                {
                    "id": data.id,
                    "name": data.name,
                    "ip_address": data.ip_address,
                    "is_alive": data.is_alive,
                    "created": data.created,
                    "modified": data.modified,
                    "count": count,
                }
            )

        return result

    def remove_server(self, *, id: str):
        from app.services.service_services import service_services

        service_services.remove_by_server(server_id=id)
        return super().remove(id=id)


server_services = CRUDServer(Server)
