"""Initial schema

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # catalogues  (reference data — frequencies, categories, habit types)
    # ------------------------------------------------------------------
    op.create_table(
        "catalogues",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("catalogue_type", sa.String(50), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_catalogues_type", "catalogues", ["catalogue_type"])

    # ------------------------------------------------------------------
    # users
    # ------------------------------------------------------------------
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("username", sa.String(100), nullable=False, unique=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"])

    # ------------------------------------------------------------------
    # habits
    # ------------------------------------------------------------------
    op.create_table(
        "habits",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("habit_name", sa.String(200), nullable=False),
        sa.Column("habit_description", sa.Text, nullable=True),
        sa.Column("frequency_id", UUID(as_uuid=True), sa.ForeignKey("catalogues.id"), nullable=False),
        sa.Column("category_id", UUID(as_uuid=True), sa.ForeignKey("catalogues.id"), nullable=False),
        sa.Column("habit_type_id", UUID(as_uuid=True), sa.ForeignKey("catalogues.id"), nullable=True),
        sa.Column("goal_target", sa.Float, nullable=True),
        sa.Column("habit_start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("habit_end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean, server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_habits_user_id", "habits", ["user_id"])

    # ------------------------------------------------------------------
    # habit_logs  (status enum: not_done | partial | done)
    # ------------------------------------------------------------------
    op.create_table(
        "habit_logs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("habit_id", UUID(as_uuid=True), sa.ForeignKey("habits.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.Enum("not_done", "partial", "done", name="completion_status"), nullable=False),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("completion_value", sa.Float, nullable=True),
        sa.Column("logged_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_habit_logs_habit_id", "habit_logs", ["habit_id"])

    # ------------------------------------------------------------------
    # streaks
    # ------------------------------------------------------------------
    op.create_table(
        "streaks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("habit_id", UUID(as_uuid=True), sa.ForeignKey("habits.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("current_streak", sa.Integer, server_default="0", nullable=False),
        sa.Column("best_streak", sa.Integer, server_default="0", nullable=False),
        sa.Column("last_completed_date", sa.Date, nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ------------------------------------------------------------------
    # rewards
    # ------------------------------------------------------------------
    op.create_table(
        "rewards",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reward_type", sa.String(50), nullable=False),
        sa.Column("amount", sa.Integer, server_default="1", nullable=False),
        sa.Column("reason", sa.String(100), nullable=True),
        sa.Column("earned_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_rewards_user_id", "rewards", ["user_id"])

    # ------------------------------------------------------------------
    # predictions
    # ------------------------------------------------------------------
    op.create_table(
        "predictions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("habit_id", UUID(as_uuid=True), sa.ForeignKey("habits.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("predicted_success", sa.Float, nullable=False),
        sa.Column("model_version", sa.String(20), nullable=True),
        sa.Column("features_snapshot", JSONB, nullable=True),
        sa.Column("predicted_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("predicted_success BETWEEN 0.0 AND 1.0", name="ck_predicted_success_range"),
    )

    # ------------------------------------------------------------------
    # Seed catalogue data
    # ------------------------------------------------------------------
    op.execute("""
        INSERT INTO catalogues (id, catalogue_type, name) VALUES
            ('00000000-0000-0000-0000-000000000001', 'frequency', 'Daily'),
            ('00000000-0000-0000-0000-000000000002', 'frequency', 'Weekly'),
            ('00000000-0000-0000-0000-000000000003', 'frequency', 'Weekdays'),
            ('00000000-0000-0000-0000-000000000010', 'category', 'Health'),
            ('00000000-0000-0000-0000-000000000011', 'category', 'Learning'),
            ('00000000-0000-0000-0000-000000000012', 'category', 'Mindfulness'),
            ('00000000-0000-0000-0000-000000000013', 'category', 'Fitness'),
            ('00000000-0000-0000-0000-000000000020', 'habit_type', 'Binary'),
            ('00000000-0000-0000-0000-000000000021', 'habit_type', 'Quantity'),
            ('00000000-0000-0000-0000-000000000022', 'habit_type', 'Duration')
    """)


def downgrade() -> None:
    op.drop_table("predictions")
    op.drop_table("rewards")
    op.drop_table("streaks")
    op.drop_table("habit_logs")
    op.execute("DROP TYPE IF EXISTS completion_status")
    op.drop_table("habits")
    op.drop_table("users")
    op.drop_table("catalogues")
