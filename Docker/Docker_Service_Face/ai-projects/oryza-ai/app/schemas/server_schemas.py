from typing import Optional
from app.schemas.base_schemas import BaseSchema
from odmantic import ObjectId
from datetime import datetime


# shared properties
class ServerBase(BaseSchema):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    is_alive: Optional[bool] = False


class ServerCreate(ServerBase):
    name: str
    ip_address: str


class ServerUpdate(ServerBase):
    pass


class ServerInDBBase(ServerBase):
    id: ObjectId


class ServerInDB(ServerInDBBase):
    pass


class ServerOut(ServerInDBBase):
    created: datetime
    modified: datetime

class ServerOutDetail(ServerOut):
    count: Optional[int] = None
    pass
class ListServerOut(BaseSchema):
    data: list[ServerOutDetail]
