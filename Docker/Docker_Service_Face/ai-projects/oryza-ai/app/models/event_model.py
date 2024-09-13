from typing import Dict, Any
from odmantic import Field, Model, Reference
from datetime import datetime

from app.models.type_service_model import TypeService
from app.common.utils.utils import datetime_now_sec
from app.models.company_model import Company


class Event(Model):
    type_service: TypeService = Reference()
    data: Dict[str, Any]
    camera: str  # camera_id
    company: Company = Reference()
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
