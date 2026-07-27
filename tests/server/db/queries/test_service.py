import pytest
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from server.db.queries.service import (
    insert_service,
)
from server.db.schema.tables.service import Service
from server.db.schema.tables.user import User


def test_insert_service(db_session):
    query = select(func.count()).select_from(Service)
    record_count = db_session.scalar(query)
    assert record_count == 0

    email = "john@example.com"
    api_key = "abcde"
    new_user = User(email=email, api_key=api_key)
    db_session.add(new_user)
    db_session.flush()

    name = "Service 1"
    inserted_service = insert_service(db_session, new_user.id, name)
    assert inserted_service is not None
    assert inserted_service.name == name

    query = select(func.count()).select_from(Service)
    record_count = db_session.scalar(query)
    assert record_count == 1

    queried_service = db_session.query(Service).filter_by(user_id=new_user.id).first()
    assert queried_service is not None
    assert queried_service.name == name
