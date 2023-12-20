from pydantic import BaseModel


class OperationBase(BaseModel):
    user_id: int
    figi: str
    price: float
    amount: int


class OperationModel(OperationBase):
    id: int
    time: float
