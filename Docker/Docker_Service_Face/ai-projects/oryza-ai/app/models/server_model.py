from app.common.utils.utils import datetime_now_sec
from odmantic import Field, Model
from datetime import datetime


class Server(Model):
    name: str
    ip_address: str
    is_alive: bool
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
