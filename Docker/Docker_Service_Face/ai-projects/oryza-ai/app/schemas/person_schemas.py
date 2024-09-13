from typing import Optional

from pydantic import BaseModel

class PersonBase(BaseModel):
    name: Optional[str] = None
    other_info: Optional[dict] = None

class PersonRegister(BaseModel):
    name: str
    data: list[str]


class PersonModify(BaseModel):
    name: Optional[str] = None
    data: list[str]
    user_id: str

class PersonUpdate(PersonBase):
    pass