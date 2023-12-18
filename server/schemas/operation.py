from pydantic import BaseModel


class OperationBase(BaseModel):
    user_id: int
    figi: str
    price: int
    amount: int


class OperationModel(OperationBase):
    id: int
    time: float
