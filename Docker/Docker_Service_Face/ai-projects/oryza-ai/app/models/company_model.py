from datetime import datetime
from odmantic import Model, Field
from typing import Optional
from app.common.utils.utils import datetime_now_sec


class Company(Model):
    name: str
    domain: str
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
    deleted: Optional[datetime] = Field(default=None)
