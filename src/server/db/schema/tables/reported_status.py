from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from server.db.schema.base import Base


MAX_NAME_LENGTH = 100

class ReportedStatus(Base):
    __tablename__ = "reported_status"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    code: Mapped[str] = mapped_column(
        String(MAX_NAME_LENGTH),
        nullable=False,
        unique=True,
    )
    name: Mapped[str] = mapped_column(
        String(MAX_NAME_LENGTH),
        nullable=False,
        unique=True,
    )
