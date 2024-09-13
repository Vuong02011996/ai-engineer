from typing import Dict, Any
from odmantic import Field, Model, Reference
from datetime import datetime
from typing import Optional
from app.models.brand_camera_model import BrandCamera
from app.models.company_model import Company
from app.common.utils.utils import datetime_now_sec


class Camera(Model):
    name: str
    ip_address: str
    port: Optional[int]
    username: str
    password: str
    rtsp: str
    rtsp_vms: Optional[str]
    company: Company = Reference()
    brand_camera: BrandCamera = Reference()
    vms_type: Optional[str]
    ward_id: Optional[str]
    is_ai: bool
    other_info: Dict[str, Any]
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
