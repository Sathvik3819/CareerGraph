import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.database import Base


class ResumeRecord(Base):
    __tablename__ = "resume_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    candidate_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    job_role: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    job_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    template: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="modern",
    )

    iterations: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    candidate_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    resume_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    review_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    
    user_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("users.id"),
    nullable=False,
    index=True,
    )

    ats_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )