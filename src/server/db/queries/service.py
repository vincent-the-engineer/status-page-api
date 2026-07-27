from uuid import uuid4

from sqlalchemy.orm import Session

from server.db.schema.tables.service import Service


def insert_service(
    session: Session,
    user_id: uuid4,
    service_name: str
) -> Service:
    new_service = Service(user_id=user_id, name=service_name)
    session.add(new_service)
    session.flush()
    return new_service
