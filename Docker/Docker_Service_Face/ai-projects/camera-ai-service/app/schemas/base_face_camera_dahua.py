from pydantic import BaseModel


class BaseCameraDahua(BaseModel):
    host: str
    username: str
    password: str
