import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

import server.db.database as db


def test_engine():
    assert db.db_engine is not None and isinstance(db.db_engine, Engine)

def test_session_factory():
    with db.SessionFactory() as session:
        assert session is not None and isinstance(session, Session)
