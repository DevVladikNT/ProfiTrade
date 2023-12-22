import time

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from crud import users
from db.base import Token
from db.session import get_db
from schemas.user import UserCreate, UserModel, UserBaseDevice

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


@router.post('/users',
             response_model=UserModel,
             status_code=201,
             tags=['user'],
             summary='Create user')
async def create(db: Session = Depends(get_db),
                 data: UserCreate = None):
    user = users.create_user(db, data)
    if not user:
        raise HTTPException(status_code=404)
    return user


@router.get('/users/{id}',
            response_model=UserModel,
            tags=['user'],
            summary='Find user')
async def read(db: Session = Depends(get_db),
               id: int = None,
               device: str = None):
    if not check(db, id, device):
        raise HTTPException(status_code=403)

    user = users.read_user(db, id)
    if not user:
        raise HTTPException(status_code=404)
    return user


@router.put('/users/{id}',
            tags=['user'],
            summary='Update user')
async def update(db: Session = Depends(get_db),
                 id: int = None,
                 data: UserBaseDevice = None):
    if not check(db, id, data.device):
        raise HTTPException(status_code=403)

    user = users.update_user(db, id, data)
    if not user:
        raise HTTPException(status_code=404)
    return Response(status_code=204)


@router.delete('/users/{id}',
               tags=['user'],
               summary='Delete user')
async def delete(db: Session = Depends(get_db),
                 id: int = None):
    rows_count = users.delete_user(db, id)
    if not rows_count:
        raise HTTPException(status_code=404)
    return Response(status_code=204)


