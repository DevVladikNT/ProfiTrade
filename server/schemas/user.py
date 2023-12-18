from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    language_code: str


class UserCreate(UserBase):
    id: int

