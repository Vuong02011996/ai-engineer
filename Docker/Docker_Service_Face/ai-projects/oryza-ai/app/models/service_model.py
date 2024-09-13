from app.common.constants.enums import TypeServiceEnum
from app.models.type_service_model import TypeService
from app.common.utils.utils import datetime_now_sec
from odmantic import Field, Model, Reference
from datetime import datetime
from app.models.server_model import Server


class Service(Model):
    name: str
    port: str
    is_alive: bool
    max_process: int
    type_service: TypeService = Reference()
    server: Server = Reference()
    type: TypeServiceEnum = Field(default=TypeServiceEnum.ai_service)
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
