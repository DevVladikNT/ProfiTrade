from sqlalchemy.orm import Session

from db.base import Operation
from schemas.user import OperationBase


def create_operation(db: Session, data: OperationBase):
    operation = Operation(
        user_id=data.user_id,
        figi=data.figi,
        type=data.type,
        price=data.price,
        amount=data.amount,
    )

    try:
        db.add(operation)
        db.commit()
        db.refresh(operation)
    except Exception as e:
        print(e)

    return operation


def read_operations(db: Session, user_id: int):
    return db.query(Operation).filter(Operation.user_id == user_id).all()
