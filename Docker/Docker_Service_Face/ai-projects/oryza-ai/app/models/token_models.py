from pydantic import BaseModel
from odmantic import ObjectId


class Token(BaseModel):
    # TODO: access_token should be a SecretStr
    access_token: str
    # refresh_token: SecretStr | None = None
    token_type: str
    expire: int


class TokenPayload(BaseModel):
    sub: ObjectId | None = None
    refresh: bool | None = False
    totp: bool | None = False


class WebToken(BaseModel):
    claim: str
