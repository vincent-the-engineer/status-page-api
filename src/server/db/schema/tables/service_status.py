from datetime import datetime
from uuid import uuid4

from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import func

from server.db.schema.base import Base


class ServiceStatus(Base):
    __tablename__ = "service_status"
    id: Mapped[uuid4] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4,
    )
    service_id: Mapped[uuid4] = mapped_column(
        ForeignKey("service.id", ondelete="CASCADE"),
    )
    reported_status_id: Mapped[uuid4] = mapped_column(
        ForeignKey("reported_status.id", ondelete="CASCADE"),
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    service: Mapped["Service"] = relationship()
    reported_status: Mapped["ReportedStatus"] = relationship()
