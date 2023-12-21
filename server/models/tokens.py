from sqlalchemy import Column, Integer, Float, String, ForeignKey

from db.base import Base


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    code = Column(String)
    secret = Column(String)
    created = Column(Float)
    expires = Column(Float)
    device = Column(String)


