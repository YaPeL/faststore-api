from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import databases

from app.config import Config

config = Config()


def get_engine(connect_args=None):
    return create_engine(config.get("SQLALCHEMY_DATABASE_URL"), connect_args=connect_args or dict())


def get_connection():
    return get_engine().connect()


def session_local_class(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session_local_class(get_engine())()
    try:
        yield db
    finally:
        db.close()


def get_database():
    return databases.Database(config.get("SQLALCHEMY_DATABASE_URL"))

