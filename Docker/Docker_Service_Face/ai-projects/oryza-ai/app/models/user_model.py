from pydantic import EmailStr
from odmantic import Field, Model, Reference
from datetime import datetime
from typing import Optional

from app.common.utils.utils import datetime_now_sec
from app.models.company_model import Company


class User(Model):
    # User INHERIT from Model instead of Base, just define like this for now,
    # dont know why inheritance from Base is not working, the program not recognize the model as a ODM model
    full_name: Optional[str] = None
    username: str
    email: EmailStr
    company: Company = Reference()
    email_validated: bool = Field(default=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_admin: bool = Field(default=False)
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
    hashed_password: str
    avatar: Optional[str] = None
