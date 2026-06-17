import pytest
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from server.db.queries.user import (
    find_user_by_email,
    insert_user,
)
from server.db.schema.tables.user import User


def test_find_user_by_email(db_session):
    email = "john.doe@example.com"
    api_key = "1234567"
    user = find_user_by_email(db_session, email)
    assert user is None
    new_user = User(email=email, api_key=api_key)
    db_session.add(new_user)
    db_session.flush()
    user = find_user_by_email(db_session, email)
    assert user is not None and user.email == email and user.api_key == api_key
    user2 = find_user_by_email(db_session, "jane@example.org")
    assert user2 is None

def test_insert_user(db_session):
    query = select(func.count()).select_from(User)
    record_count = db_session.scalar(query)
    assert record_count == 0

    email = "john@example.com"
    api_key = "abcde"
    inserted_user = insert_user(db_session, email, api_key)
    assert inserted_user.id is not None
    assert inserted_user.email == email
    assert inserted_user.api_key == api_key
    assert inserted_user.created_at is not None
    assert inserted_user.updated_at is not None

    query = select(func.count()).select_from(User)
    record_count = db_session.scalar(query)
    assert record_count == 1

    queried_user = db_session.query(User).filter_by(email=email).first()
    assert queried_user is not None
    assert queried_user.email == email

def test_insert_user_duplicated_email(db_session):
    query = select(func.count()).select_from(User)
    record_count = db_session.scalar(query)
    assert record_count == 0

    email = "jane@example.org"
    api_key1 = "abcde"
    inserted_user = insert_user(db_session, email, api_key1)
    assert inserted_user.id is not None
    assert inserted_user.email == email
    assert inserted_user.api_key == api_key1
    assert inserted_user.created_at is not None
    assert inserted_user.updated_at is not None

    api_key2 = "xyz"
    with pytest.raises(IntegrityError):
        inserted_user2 = insert_user(db_session, email, api_key2)
