from sqlalchemy import Column, ForeignKey, Integer, Float, String

from db.base import Base


class Operation(Base):
    __tablename__ = 'operations'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    figi = Column(String(12))
    price = Column(Float)
    amount = Column(Integer)
    time = Column(Float)

