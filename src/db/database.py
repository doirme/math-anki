
from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
def make_sqlite_engine(path: str, echo: bool = False):
    return create_engine(f"sqlite:///{path}", echo=echo, future=True)
def make_session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)
