from datetime import datetime

from odmantic import Field, Model, Reference

from app.common.utils.utils import datetime_now_sec
from app.models import Camera
from app.models.type_service_model import TypeService


class CameraTypeAIMapping(Model):
    camera: Camera = Reference()
    type_service: TypeService = Reference()
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
