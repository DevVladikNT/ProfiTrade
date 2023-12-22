import rsa
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import tokens
from db.session import get_db
from schemas.token import TokenCreate, TokenUpdate, MessageEncode

router = APIRouter()


@router.post('/tokens',
             status_code=201,
             tags=['token'],
             summary='Create token')
def create(db: Session = Depends(get_db),
           data: TokenCreate = None):
    code = tokens.create_token(db, data)
    if not code:
        raise HTTPException(status_code=403)
    return code


@router.put('/tokens',
            status_code=202,
            tags=['token'],
            summary='Update token')
def update(db: Session = Depends(get_db),
           data: TokenUpdate = None):
    user_id = tokens.update_token(db, data)
    if not user_id:
        raise HTTPException(status_code=403)
    return user_id


@router.post('/encrypt',
             tags=['token'],
             summary='Encrypt message')
def encrypt(data: MessageEncode = None):
    params = data.key.split('.')
    if len(params) != 2:
        raise HTTPException(status_code=400)
    pub = rsa.PublicKey(int(params[0]), int(params[1]))
    crypto = rsa.encrypt(data.message.encode(), pub)
    string = str(crypto)
    return string
