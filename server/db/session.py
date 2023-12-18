from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, Session

URL_DATABASE = 'sqlite:///../ProfiTrade_tools/database.db'

engine = create_engine(URL_DATABASE, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    with SessionLocal() as session:
        yield session
