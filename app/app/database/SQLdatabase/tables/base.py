from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
import datetime
from uuid import uuid4
import sqlalchemy as sa
import os


url = URL.create(
    drivername = "postgresql",
    host = os.environ.get('PGVECTOR_HOST'),
    username = os.environ.get('PGVECTOR_USER'),
    password = os.environ.get('PGVECTOR_PASSWORD'),
    database = os.environ.get('PGVECTOR_DATABASE'),
    port = int(os.environ.get("PGVECTOR_PORT", "5432"))
)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class SQLBaseModel(Base):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.utcnow)
    deleted = sa.Column(sa.DateTime(timezone=True), default=None)


def get_table_dict(obj:SQLBaseModel) -> dict:
    return {c.key : getattr(obj,c.key) for c in inspect(obj).mapper.column_attrs}

def get_uuid4() -> str:
    return str(uuid4())
