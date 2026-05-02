import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base import Base, TimestampMixin

import enum


class CompletionStatusEnum(str, enum.Enum):
    NOT_DONE = "not_done"
    PARTIAL = "partial"
    DONE = "done"


class HabitLogModel(Base):
    __tablename__ = "habit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    habit_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("habits.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[CompletionStatusEnum] = mapped_column(
        Enum(CompletionStatusEnum, name="completion_status", values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    completion_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    habit: Mapped["HabitModel"] = relationship(  # type: ignore[name-defined]
        "HabitModel", back_populates="logs"
    )
