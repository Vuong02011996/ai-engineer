from pydantic import BaseModel


class BaseSchema(BaseModel):
    pass


class Msg(BaseSchema):
    msg: str


class Count(BaseSchema):
    count: int
