import time
import rsa

from sqlalchemy.orm import Session

from db.base import Token, User
from schemas.token import TokenCreate, TokenUpdate


def create_token(db: Session, data: TokenCreate):
    user = db.query(User).get(data.user_id)
    if not user:
        return None
    (pub, priv) = rsa.newkeys(512)
    token = Token(
        user_id=user.id,
        code=f'{pub.n}.{pub.e}',
        secret=f'{priv.n}.{priv.e}.{priv.d}.{priv.p}.{priv.q}',
        created=time.time(),
        expires=(time.time() + 60 * data.time_delta),
        device='',
    )

    try:
        db.add(token)
        db.commit()
        db.refresh(token)
    except Exception as e:
        print(e)
        return None

    return token.code


def update_token(db: Session, data: TokenUpdate):
    token = (db.query(Token)
             .filter(Token.code == data.code)
             .order_by(Token.created.desc())
             .first())
    if not token:
        return None
    elif token.expires < time.time():
        return None

    params = token.secret.split('.')
    priv = rsa.PrivateKey(
        int(params[0]),
        int(params[1]),
        int(params[2]),
        int(params[3]),
        int(params[4])
    )
    crypto = eval(data.message)
    text = rsa.decrypt(crypto, priv)
    if token.device not in [text, '']:
        return None
    token.device = text

    try:
        db.add(token)
        db.commit()
        db.refresh(token)
    except Exception as e:
        print(e)
        return None

    return token.user_id

