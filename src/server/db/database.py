import atexit
from typing import Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session


db_engine: Optional[Engine] = None
SessionFactory: Optional[Session] = None

def init_db(database_url: str) -> None:
    global db_engine
    if db_engine is None:
        db_engine = create_engine(database_url, echo=True)
        atexit.register(db_engine.dispose)
        print("Database engine initialised.")
    else:
        print("Engine is already initialised.")

    global SessionFactory
    if SessionFactory is None:
        SessionFactory = sessionmaker(bind=db_engine)
        print("Session factory initalised.")
    else:
        print("Session factory is already intialised.")
