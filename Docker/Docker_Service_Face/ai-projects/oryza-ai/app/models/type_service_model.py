from odmantic import Field, Model
from datetime import datetime
from app.common.utils.utils import datetime_now_sec


class TypeService(Model):
    name: str
    key: str
    modified: datetime = Field(default_factory=datetime_now_sec)
    created: datetime = Field(default_factory=datetime_now_sec)
