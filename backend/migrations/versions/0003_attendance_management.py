"""Add attendance location and policy management."""

from alembic import op
import sqlalchemy as sa


revision = "0003_attendance"
down_revision = "0002_budget_permissions"
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    attendance_columns = {column["name"] for column in inspector.get_columns("attendance")}
    if "work_location" not in attendance_columns:
        op.add_column("attendance", sa.Column("work_location", sa.String(100), nullable=True))

    if "attendance_policies" not in inspector.get_table_names():
        op.create_table(
            "attendance_policies",
            sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
            sa.Column("name", sa.String(150), nullable=False, unique=True),
            sa.Column("count_type", sa.String(30), nullable=False, server_default="daily"),
            sa.Column("considerable_value", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("adjusted_days", sa.Numeric(6, 2), nullable=False, server_default="0"),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.Column("deleted_at", sa.DateTime(), nullable=True),
            mysql_charset="utf8mb4",
            mysql_collate="utf8mb4_unicode_ci",
        )
        op.create_index("ix_attendance_policies_is_active", "attendance_policies", ["is_active"])
        op.create_index("ix_attendance_policies_deleted_at", "attendance_policies", ["deleted_at"])


def downgrade():
    op.drop_table("attendance_policies")
    op.drop_column("attendance", "work_location")
