from sqlalchemy.orm import Session

from db.base import User
from schemas.user import UserBaseDevice, UserCreate


def create_user(db: Session, data: UserCreate):
    user = User(
        id=data.id,
        username=data.username,
        language_code=data.language_code,
        balance=10000.0,
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        print(e)

    return user


def read_user(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


def update_user(db: Session, id: int, data: UserBaseDevice):
    user = db.query(User).get(id)
    if not user:
        return None
    user.username = data.username
    user.language_code = data.language_code
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        print(e)
        return None

    return user


def delete_user(db: Session, id: int):
    rows_count = db.query(User).filter(User.id == id).delete()
    db.commit()
    return rows_count

