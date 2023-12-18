from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from crud import users
from db.session import get_db
from schemas.user import UserBase, UserCreate, UserModel

router = APIRouter()


@router.post('/users',
             response_model=UserModel,
             status_code=201,
             tags=['user'],
             summary='Create user')
async def create(db: Session = Depends(get_db), data: UserCreate = None):
    user = users.create_user(db, data)
    if not user:
        raise HTTPException(status_code=404)
    return user


@router.get('/users/{id}',
            response_model=UserModel,
            tags=['user'],
            summary='Find user')
async def read(db: Session = Depends(get_db), id_: int = None):
    user = users.read_user(db, id_)
    if not user:
        raise HTTPException(status_code=404)
    return user


@router.put('/users/{id}',
            tags=['user'],
            summary='Update user')
async def update(db: Session = Depends(get_db), id_: int = None, data: UserBase = None):
    user = users.update_user(db, id_, data)
    if not user:
        raise HTTPException(status_code=404)
    return Response(status_code=204)


@router.delete('/users/{id}',
               tags=['user'],
               summary='Delete user')
async def delete(db: Session = Depends(get_db), id_: int = None):
    rows_count = users.delete_user(db, id_)
    if not rows_count:
        raise HTTPException(status_code=404)
    return Response(status_code=204)


