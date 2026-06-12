from sqlalchemy.orm import Session

from server.db.schema.tables.user import User


def find_user_by_email(session: Session, email: str) -> User:
    pass

def insert_user(session: Session, email: str, api_key: str) -> User:
    new_user = User(email=email, api_key=api_key)
    session.add(new_user)
    session.flush()
    return new_user
