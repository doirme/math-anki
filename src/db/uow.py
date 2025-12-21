
from __future__ import annotations
from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session

class UnitOfWork(AbstractContextManager):
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory
        self.session: Session | None = None
    def __enter__(self) -> "UnitOfWork":
        self.session = self._session_factory()
        return self
    def __exit__(self, exc_type, exc, tb) -> None:
        assert self.session is not None
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
        self.session = None
