from app.models import Camera
from app.common.utils.utils import datetime_now_sec
from odmantic import Field, Model, Reference, ObjectId
from datetime import datetime


class SettingUniformsCompany(Model):
    rgb: str
    id_company: str
    list_image: list[str]
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
