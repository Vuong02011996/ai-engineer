from datetime import datetime
from odmantic import Model, Field, Reference
from typing import Optional
from app.common.constants.enums import ProcessStatus
from app.models import Company
from app.models.camera_model import Camera
from app.models.service_model import Service
from app.common.utils.utils import datetime_now_sec


class Process(Model):
    camera: Camera = Reference()
    status: ProcessStatus = Field(default=ProcessStatus.stop)
    isEnable: bool = Field(default=False)
    service: Service = Reference()
    pid: str = Field(default="")
    id_type_service: str = Field(default="")
    company: Company = Reference()
    is_debug: bool = Field(default=False)
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
    rtsp: Optional[str] = Field(default=None)
