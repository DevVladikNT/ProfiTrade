from pydantic import BaseModel


class OperationBase(BaseModel):
    user_id: int
    figi: str
    price: float
    amount: int
    device: str


class OperationModel(OperationBase):
    id: int
    time: float
