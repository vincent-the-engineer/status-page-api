from uuid import uuid4

from sqlalchemy.orm import Session

from server.db.schema.tables.service_status import ServiceStatus


def insert_service_status(
    session: Session,
    service_id: uuid4,
    reported_status_id: int
) -> ServiceStatus:
    new_service_status = ServiceStatus(
        service_id=service_id,
        reported_status_id=reported_status_id
    )
    session.add(new_service_status)
    session.flush()
    return new_service_status
