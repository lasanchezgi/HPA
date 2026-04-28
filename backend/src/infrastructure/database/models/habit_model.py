import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base import Base, TimestampMixin


class HabitModel(TimestampMixin, Base):
    __tablename__ = "habits"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    habit_name: Mapped[str] = mapped_column(String(200), nullable=False)
    habit_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    frequency_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    habit_type_id: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    goal_target: Mapped[float | None] = mapped_column(Float, nullable=True)
    habit_start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    habit_end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["UserModel"] = relationship(  # type: ignore[name-defined]
        "UserModel", back_populates="habits"
    )
    logs: Mapped[list["HabitLogModel"]] = relationship(  # type: ignore[name-defined]
        "HabitLogModel", back_populates="habit", lazy="selectin"
    )
