from datetime import datetime
from typing import Dict, Any

from odmantic import Field, Model

from app.common.utils import datetime_now_sec


class Person(Model):
    name: str
    company_id: str
    other_info: Dict[str, Any]
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
    is_delete: bool = Field(default=False)


