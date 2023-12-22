import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import operations
from db.base import Token
from db.session import get_db
from schemas.operation import OperationBase

router = APIRouter()


def check(db: Session,
          id: int,
          device: str) -> bool:
    token = (db.query(Token)
             .filter(Token.user_id == id)
             .order_by(Token.created.desc())
             .first())
    if not token:
        return False
    elif token.expires < time.time() or token.device != device.encode():
        return False
    return True


@router.post('/operations',
             status_code=201,
             tags=['operation'],
             summary='Create operation')
async def create(db: Session = Depends(get_db),
                 data: OperationBase = None):
    if not check(db, data.user_id, data.device):
        raise HTTPException(status_code=403)

    operation = operations.create_operation(db, data)
    if not operation:
        raise HTTPException(status_code=403)
    return operation


@router.get('/operations/{user_id}',
            tags=['operation'],
            summary='List of user\'s operations')
async def read(db: Session = Depends(get_db),
               user_id: int = None,
               device: str = None):
    if not check(db, user_id, device):
        raise HTTPException(status_code=403)

    data = operations.read_operations(db, user_id)
    if not data:
        return []
    return data


