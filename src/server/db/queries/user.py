from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session

from server.db.schema.tables.user import User
from server.utils.auth import (
    hash_api_key,
    verify_api_key,
)


def delete_user_by_email(session: Session, email: str) -> None:
    query = delete(User).where(
        func.lower(User.email) == func.lower(email)
    )
    session.execute(query)
    session.flush()

def find_user_by_email(session: Session, email: str) -> User:
    query = select(User).where(
        func.lower(User.email) == func.lower(email)
    )
    user = session.scalars(query).one_or_none()
    return user

def insert_user(session: Session, email: str, api_key: str) -> User:
    hash = hash_api_key(api_key)
    new_user = User(email=email, api_key=hash)
    session.add(new_user)
    session.flush()
    return new_user

def verify_user(user: User, api_key: str) -> bool:
    return verify_api_key(api_key, user.api_key)
