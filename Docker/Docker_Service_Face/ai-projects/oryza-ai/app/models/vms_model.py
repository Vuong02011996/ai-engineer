from app.common.utils.utils import datetime_now_sec
from datetime import datetime
from odmantic import Model, Field


class VMS(Model):
    username: str
    password: str
    ip_address: str
    port: int
    vms_type: str
    company_id: str
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)


# nx_oryza
# username: admin
# password: oryza@2023
# url: https://192.168.111.63:7001
