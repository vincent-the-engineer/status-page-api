from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import func

from server.db.schema.base import Base


# RFC 5321 specifies email address must fit within 256 characters
# that includes "<" and ">".
MAX_EMAIL_LENGTH = 254

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid4] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(MAX_EMAIL_LENGTH),
        nullable=False,
        unique=True,
    )
    # Hash of the API key
    api_key: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
