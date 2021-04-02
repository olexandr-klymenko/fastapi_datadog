from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = environ.get(
    "SQLALCHEMY_DATABASE_URL", "postgresql+pg8000://postgres:postgres@postgres/rainbow_database"
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, client_encoding='utf8'
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
