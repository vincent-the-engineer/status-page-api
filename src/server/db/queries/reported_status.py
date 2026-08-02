from typing import Final
from sqlalchemy.orm import Session

from server.db.schema.tables.reported_status import ReportedStatus


HEALTHY_STATUS_ID: Final[int] = 1
DEGRADED_STATUS_ID: Final[int] = 2
MAINTENANCE_STATUS_ID: Final[int] = 3
STOPPED_STATUS_ID: Final[int] = 4

HEALTHY_STATUS_CODE: Final[str] = "HEALTHY"
DEGRADED_STATUS_CODE: Final[str] = "DEGRADED"
MAINTENANCE_STATUS_CODE: Final[str] = "MAINTENANCE"
STOPPED_STATUS_CODE: Final[str] = "STOPPED"

def initialise_reported_status(session: Session) -> None:
    STATUSES = [
        {
            "id": HEALTHY_STATUS_ID,
            "code": HEALTHY_STATUS_CODE,
            "name": "Healthy",
        },
        {
            "id": DEGRADED_STATUS_ID,
            "code": DEGRADED_STATUS_CODE,
            "name": "Degraded",
        },
        {
            "id": MAINTENANCE_STATUS_ID,
            "code": MAINTENANCE_STATUS_CODE,
            "name": "Maintenance",
        },
        {
            "id": STOPPED_STATUS_ID,
            "code": STOPPED_STATUS_CODE,
            "name": "Stopped",
        },
    ]
    for status in STATUSES:
        session.merge(ReportedStatus(**status))
    session.commit()
