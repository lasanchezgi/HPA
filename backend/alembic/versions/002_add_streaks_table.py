"""Add streaks table (Session 3 — persist streak in DB)

Revision ID: 002
Revises: 001
Create Date: 2026-04-29
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "streaks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "habit_id",
            UUID(as_uuid=True),
            sa.ForeignKey("habits.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("current_streak", sa.Integer, server_default="0", nullable=False),
        sa.Column("best_streak", sa.Integer, server_default="0", nullable=False),
        sa.Column("last_completed_date", sa.Date, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_streaks_habit_id", "streaks", ["habit_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_streaks_habit_id", table_name="streaks")
    op.drop_table("streaks")
