import os

import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine

import server.db.database as db


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_database():
    # ---- SETUP ----
    TEST_DATABASE_URL = os.getenv("DATABASE_URL")
    db.init_db(TEST_DATABASE_URL)
    assert db.db_engine is not None
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)    
    # Run the migrations up to the latest version
    command.upgrade(alembic_cfg, "head")
    print("\n[Setup] Database opened and tables created.")

    yield
    
    # ---- TEARDOWN ----
    # Rollback all migrations after the test session finishes
    command.downgrade(alembic_cfg, "base")
    db.db_engine.dispose()
    print("\n[Teardown] Database tables dropped and connections closed.")
