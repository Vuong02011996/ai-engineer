from typing import Optional

from bson import ObjectId
from pydantic import BaseModel

from app.schemas.base_schemas import BaseSchema





class SettingUniformsCompanyCreate(BaseModel):
    rgb: str
    id_company: str
    list_image: list[str]


class SettingUniformsCompanyUpdate(BaseModel):
    rgb: str

class SettingUniformsCompanyDeleteImage(BaseModel):
    image_url: str
