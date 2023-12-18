import time

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from db.base import Operation, User
from schemas.operation import OperationBase


def create_operation(db: Session, data: OperationBase):
    user = db.query(User).get(data.user_id)
    if not user:
        return None
    user.balance -= data.amount * data.price
    if user.balance < 0:
        return None
    available = (db.query(func.sum(Operation.amount))
                 .filter(Operation.user_id == User.id and Operation.figi == data.figi)
                 .first())
    # If we want to sell more than we have
    if available[0] < data.amount * -1:
        return None
    operation = Operation(
        user_id=data.user_id,
        figi=data.figi,
        price=data.price,
        amount=data.amount,
        time=time.time()
    )

    try:
        db.add(user)
        db.add(operation)
        db.commit()
        db.refresh(user)
        db.refresh(operation)
    except Exception as e:
        print(e)
        return None

    return operation


def read_operations(db: Session, user_id: int):
    data = db.query(Operation).filter(Operation.user_id == user_id).all()
    if not data:
        return None
    return data
