import pytest
from sqlalchemy import select, func

from server.db.queries.reported_status import (
    get_reported_status_id,
    initialise_reported_status,
    HEALTHY_STATUS_ID,
    DEGRADED_STATUS_ID,
    MAINTENANCE_STATUS_ID,
    STOPPED_STATUS_ID,
    HEALTHY_STATUS_CODE,
    DEGRADED_STATUS_CODE,
    MAINTENANCE_STATUS_CODE,
    STOPPED_STATUS_CODE,
)
from server.db.schema.tables.reported_status import ReportedStatus


def test_get_reported_status_id():
    assert get_reported_status_id(HEALTHY_STATUS_CODE) == HEALTHY_STATUS_ID
    assert get_reported_status_id(DEGRADED_STATUS_CODE) == DEGRADED_STATUS_ID
    assert get_reported_status_id(MAINTENANCE_STATUS_CODE) == MAINTENANCE_STATUS_ID
    assert get_reported_status_id(STOPPED_STATUS_CODE) == STOPPED_STATUS_ID
    assert get_reported_status_id("test") is None
    assert get_reported_status_id("healthy") == HEALTHY_STATUS_ID

def test_initialise_reported_status(db_session):
    query = select(func.count()).select_from(ReportedStatus)
    record_count = db_session.scalar(query)
    assert record_count == 0

    initialise_reported_status(db_session)

    query = select(func.count()).select_from(ReportedStatus)
    record_count = db_session.scalar(query)
    assert record_count == 4

    statuses = db_session.query(ReportedStatus).order_by(ReportedStatus.id).all()
    assert statuses[0].id == HEALTHY_STATUS_ID and statuses[0].code == HEALTHY_STATUS_CODE
    assert statuses[1].id == DEGRADED_STATUS_ID and statuses[1].code == DEGRADED_STATUS_CODE
    assert statuses[2].id == MAINTENANCE_STATUS_ID and statuses[2].code == MAINTENANCE_STATUS_CODE
    assert statuses[3].id == STOPPED_STATUS_ID and statuses[3].code == STOPPED_STATUS_CODE

def test_initialise_reported_status_repeated(db_session):
    query = select(func.count()).select_from(ReportedStatus)
    record_count = db_session.scalar(query)
    assert record_count == 0

    initialise_reported_status(db_session)
    initialise_reported_status(db_session)

    query = select(func.count()).select_from(ReportedStatus)
    record_count = db_session.scalar(query)
    assert record_count == 4
