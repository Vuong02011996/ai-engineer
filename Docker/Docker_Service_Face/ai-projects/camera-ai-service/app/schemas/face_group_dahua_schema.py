from typing import Optional

from app.schemas.base_face_camera_dahua import BaseCameraDahua


class CreateFaceGroup(BaseCameraDahua):
    group_name: str
    group_detail: str


class UpdateFaceGroup(BaseCameraDahua):
    group_id: str
    group_name: str
    group_detail: Optional[str] = None

class DeleteFaceGroup(BaseCameraDahua):
    group_id: str
