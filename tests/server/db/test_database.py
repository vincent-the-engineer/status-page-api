import pytest
from sqlalchemy import Engine

import server.db.database as db


def test_engine():
    assert db.db_engine is not None and isinstance(db.db_engine, Engine)
