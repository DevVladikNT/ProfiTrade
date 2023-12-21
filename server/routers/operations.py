from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import operations
from db.session import get_db
from schemas.operation import OperationBase

router = APIRouter()


@router.post('/operations',
             status_code=201,
             tags=['operation'],
             summary='Create operation')
async def create(db: Session = Depends(get_db), data: OperationBase = None):
    operation = operations.create_operation(db, data)
    if not operation:
        raise HTTPException(status_code=403)
    return operation


@router.get('/operations/{user_id}',
            tags=['operation'],
            summary='List of user\'s operations')
async def read(db: Session = Depends(get_db), user_id: int = None):
    data = operations.read_operations(db, user_id)
    if not data:
        return []
    return data


