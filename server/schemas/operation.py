from pydantic import BaseModel


class OperationBase(BaseModel):
    user_id: int
    figi: str
    type: bool
    price: int
    amount: int
