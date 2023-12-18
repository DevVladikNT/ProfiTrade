from sqlalchemy import Column, Integer, String

from db.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    language_code = Column(String)


