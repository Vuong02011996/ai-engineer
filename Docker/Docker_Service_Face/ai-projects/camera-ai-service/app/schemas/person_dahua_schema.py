from typing import Optional

from pydantic import BaseModel

from app.schemas.base_face_camera_dahua import BaseCameraDahua


class CreatePerson(BaseModel):
    host : Optional[str] = None
    username : Optional[str] = None
    password : Optional[str] = None
    group_id: Optional[str] = None
    name: Optional[str] = None
    sex: Optional[str] = None
    birthday: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    image: Optional[bytes] = None



class UpdatePerson(CreatePerson):
    uid: Optional[str] = None



class DeletePerson(BaseCameraDahua):
    group_id: str
    uid : str

class OutsPerson(BaseCameraDahua):
    group_id: str
    page: int
