from datetime import datetime

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import func

from server.db.schema.base import Base


_MAX_NAME_LENGTH = 100

class ReportedStatus(Base):
    __tablename__ = "reported_status"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    code: Mapped[str] = mapped_column(
        String(_MAX_NAME_LENGTH),
        nullable=False,
        unique=True,
    )
    name: Mapped[str] = mapped_column(
        String(_MAX_NAME_LENGTH),
        nullable=False,
        unique=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
