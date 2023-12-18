from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import operations
from db.session import get_db
from schemas.operation import OperationBase

router = APIRouter()


@router.post('/operations', status_code=201, tags=['operation'])
async def create(db: Session = Depends(get_db), data: OperationBase = None):
    return operations.create_operation(db, data)


@router.get('/operations/{user_id}', tags=['operation'])
async def read(db: Session = Depends(get_db), user_id: int = None):
    return operations.read_operations(db, user_id)


