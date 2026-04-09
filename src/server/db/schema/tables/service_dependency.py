from uuid import uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from server.db.schema.base import Base


MAX_NAME_LENGTH = 50

class ServiceDependency(Base):
    __tablename__ = "service_dependencies"
    service_id: Mapped[uuid4] = mapped_column(
        ForeignKey("services.id", ondelete="CASCADE"),
        primary_key=True,
    )
    dependency_id: Mapped[uuid4] = mapped_column(
        ForeignKey("services.id", ondelete="CASCADE"),
        primary_key=True,
    )
