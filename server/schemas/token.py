from pydantic import BaseModel


class TokenCreate(BaseModel):
    user_id: int
    time_delta: int


class TokenUpdate(BaseModel):
    code: str
    message: str


class MessageEncode(BaseModel):
    message: str
    key: str
