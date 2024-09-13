from datetime import datetime

from odmantic import Field, Model

from app.common.utils.utils import datetime_now_sec


class BrandCamera(Model):
    name: str
    key: str
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
