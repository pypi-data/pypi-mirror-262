import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import config

engine = create_engine(config.DATABASE_URL, echo=False)  # echo=True for database debug

session_maker = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


from models.post import Post


def get_session():
    with session_maker() as session:
        yield session


def create_database():
    Base.metadata.create_all(engine)


def drop_database():
    Base.metadata.drop_all(engine)


def add_sample_data():
    if os.path.exists(config.PROJECT_ROOT + '/' + config.DATABASE_NAME):
        create_database()
        return
    create_database()
    with session_maker() as session:
        session.add_all([

        ])
