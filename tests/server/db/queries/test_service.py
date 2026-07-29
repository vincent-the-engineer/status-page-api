from uuid import uuid4

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

def test_insert_service_invalid_user_id(db_session):
    query = select(func.count()).select_from(Service)
    record_count = db_session.scalar(query)
    assert record_count == 0

    email = "john@example.com"
    api_key = "abcde"
    new_user = User(email=email, api_key=api_key)
    db_session.add(new_user)
    db_session.flush()

    random_id = uuid4()
    name = "Service 1"
    with pytest.raises(IntegrityError):
        inserted_service = insert_service(db_session, random_id, name)

def test_delete_user_cascade_delete(db_session):
    query = select(func.count()).select_from(Service)
    record_count = db_session.scalar(query)
    assert record_count == 0

    email1 = "john@example.com"
    api_key1 = "abcde"
    user1 = User(email=email1, api_key=api_key1)
    db_session.add(user1)
    email2 = "jane@example.org"
    api_key2 = "xyz"
    user2 = User(email=email2, api_key=api_key2)
    db_session.add(user2)
    db_session.flush()

    name1 = "Service 1"
    service1 = Service(user_id=user1.id, name=name1)
    db_session.add(service1)
    name2 = "Service 2"
    service2 = Service(user_id=user2.id, name=name2)
    db_session.add(service2)
    db_session.flush()

    query = select(func.count()).select_from(Service)
    record_count = db_session.scalar(query)
    assert record_count == 2

    db_session.delete(user2)
    db_session.flush()

    query = select(func.count()).select_from(Service)
    record_count = db_session.scalar(query)
    assert record_count == 1

    queried_service = db_session.query(Service).filter_by(user_id=user1.id).first()
    assert queried_service is not None
    assert queried_service.name == name1
