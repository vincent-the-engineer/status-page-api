from collections.abc import Iterator
import os
import sys
from pathlib import Path

import pytest
from alembic.config import Config
from alembic import command
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker, Session

import server.db.database as db


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_database():
    project_root = Path(__file__).resolve().parent.parent.parent
    ini_path = project_root / "alembic.ini"

    # ---- SETUP ----
    TEST_DATABASE_URL = os.getenv("DATABASE_URL")
    db.init_db(TEST_DATABASE_URL)
    assert db.db_engine is not None
    alembic_cfg = Config(str(ini_path))
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)

    # Share connection with Alembic    
    # Run the migrations up to the latest version
    with db.db_engine.begin() as connection:
        alembic_cfg.attributes["connection"] = connection
        command.upgrade(alembic_cfg, "head")    
    print("\n[Setup] Database opened and tables created.")

    yield
    
    # ---- TEARDOWN ----
    # Rollback all migrations after the test session finishes
    with db.db_engine.begin() as connection:
        alembic_cfg.attributes["connection"] = connection
        command.downgrade(alembic_cfg, "base")
    db.db_engine.dispose()
    print("\n[Teardown] Database tables dropped and connections closed.")

@pytest.fixture(scope="function")
def db_connection() -> Iterator[Connection]:
    connection = db.db_engine.connect()
    # Being a top-level transaction.
    transaction = connection.begin()

    yield connection

    # Roll back the top-level transaction.
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def db_session(db_connection: Connection) -> Iterator[Session]:
    Session = sessionmaker(bind=db_connection)
    session = Session()
    # Nested transaction savepoint
    session.begin_nested()

    # If something calls session.commit(), intercept it and start a
    # new nested transaction.
    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    yield session

    session.close()
