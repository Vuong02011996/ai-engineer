from odmantic import Field, Model, Reference
from datetime import datetime

from app.models.type_service_model import TypeService
from app.common.utils.utils import datetime_now_sec
from app.models.company_model import Company


class Webhook(Model):
    name: str
    endpoint: str
    status: bool
    type_service: TypeService = Reference()
    company: Company = Reference()
    token: str
    auth_type: str
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
