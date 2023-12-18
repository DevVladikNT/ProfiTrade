from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import users
from db.session import get_db
from schemas.user import UserBase, UserCreate

router = APIRouter()


@router.post('/users', status_code=201, tags=['user'])
async def create(db: Session = Depends(get_db), data: UserCreate = None):
    return users.create_user(db, data)


@router.get('/users/{id}', tags=['user'])
async def read(db: Session = Depends(get_db), id: int = None):
    user = users.read_user(db, id)
    if not user:
        raise HTTPException(status_code=404)
    return user


@router.put('/users/{id}', status_code=204, tags=['user'])
async def update(db: Session = Depends(get_db), id: int = None, data: UserBase = None):
    user = users.update_user(db, id, data)
    if not user:
        raise HTTPException(status_code=404)


@router.delete('/users/{id}', status_code=204, tags=['user'])
async def delete(db: Session = Depends(get_db), id: int = None):
    users.delete_user(db, id)

