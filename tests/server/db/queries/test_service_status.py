from uuid import uuid4

import pytest
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from server.db.queries.reported_status import (
    initialise_reported_status,
    HEALTHY_STATUS_ID,
    DEGRADED_STATUS_ID,
    MAINTENANCE_STATUS_ID,
    STOPPED_STATUS_ID,
)
from server.db.queries.service_status import (
    insert_service_status,
)
from server.db.schema.tables.reported_status import ReportedStatus
from server.db.schema.tables.service import Service
from server.db.schema.tables.service_status import ServiceStatus
from server.db.schema.tables.user import User


def test_insert_service_status(db_session):
    query = select(func.count()).select_from(ServiceStatus)
    record_count = db_session.scalar(query)
    assert record_count == 0

    initialise_reported_status(db_session)

    email = "john@example.com"
    api_key = "abcde"
    user = User(email=email, api_key=api_key)
    db_session.add(user)
    db_session.flush()

    name = "Service 1"
    service = Service(user_id=user.id, name=name)
    db_session.add(service)
    db_session.flush()

    status_id = HEALTHY_STATUS_ID
    service_status = insert_service_status(db_session, service.id, status_id)
    
    assert service_status is not None
    assert service_status.reported_status_id == status_id

    query = select(func.count()).select_from(ServiceStatus)
    record_count = db_session.scalar(query)
    assert record_count == 1

    queried_service_status = db_session.query(ServiceStatus).filter_by(service_id=service.id).first()
    assert queried_service_status is not None
    assert queried_service_status.reported_status_id == status_id
