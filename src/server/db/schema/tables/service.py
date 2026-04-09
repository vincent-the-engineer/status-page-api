from uuid import uuid4
from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.db.schema.base import Base


MAX_NAME_LENGTH = 50

class Service(Base):
    __tablename__ = "services"
    id: Mapped[uuid4] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH))
    user_id: Mapped[uuid4] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    owner: Mapped["User"] = relationship()
    dependencies: Mapped[list["Service"]] = relationship(
        "Service",
        secondary="service_dependencies",
        primaryjoin="Service.id == service_dependencies.c.service_id",
        secondaryjoin="Service.id == service_dependencies.c.dependency_id",
        backref="required_by",
        # Ensures the entries in the association table are cleaned up
        cascade="all, delete",
    )    
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
