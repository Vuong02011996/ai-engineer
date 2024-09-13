from typing import Optional
from pydantic import (
    Field,
    EmailStr,
    field_validator,
    SecretStr,
)
from odmantic import ObjectId
from datetime import datetime
from app.schemas.base_schemas import BaseSchema
from app.models.company_model import Company


# shared properties
class UserBase(BaseSchema):
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    email_validated: Optional[bool] = False
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_admin: Optional[bool] = False
    avatar: Optional[bytes] = None


class UserRegister(BaseSchema):
    username: str
    email: EmailStr
    password: str
    company_id: str


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str
    company_id: str
    avatar: Optional[bytes] = None
    is_admin: Optional[bool] = False


class UserUpdate(BaseSchema):
    company: Optional[str] = None
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    avatar: Optional[bytes] = None


class UserUpdateMe(BaseSchema):
    full_name: Optional[str] = None
    username: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None


class UserInDBBase(UserBase):
    id: ObjectId
    company: Company


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: Optional[SecretStr] = None


class CompanyBase(BaseSchema):
    id: ObjectId
    name: str


class UserOut(UserInDBBase):
    company: CompanyBase
    hashed_password: bool = Field(default=False, alias="password")
    created: datetime
    modified: datetime

    @field_validator("hashed_password", mode="before")
    def convert_password_to_hashed_password(cls, v):
        return True if v else False


class ListUserOut(BaseSchema):
    data: list[UserOut]


class UserLogin(BaseSchema):
    username: str
    password: str
