"""Add shift management tables."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


revision = "0004_shifts"
down_revision = "0003_attendance"
branch_labels = None
depends_on = None
BIGINT = mysql.BIGINT(unsigned=True)
TABLE_OPTIONS = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"}


def timestamps():
    return [sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False)]


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if "shifts" not in inspector.get_table_names():
        op.create_table(
            "shifts", sa.Column("id", BIGINT, primary_key=True, autoincrement=True),
            sa.Column("name", sa.String(150), nullable=False, unique=True), sa.Column("start_time", sa.Time(), nullable=False),
            sa.Column("end_time", sa.Time(), nullable=False), sa.Column("shift_type", sa.String(30), nullable=False),
            sa.Column("status", sa.String(20), nullable=False), sa.Column("notes", sa.Text()), *timestamps(),
            sa.Column("deleted_at", sa.DateTime()), **TABLE_OPTIONS,
        )
        op.create_index("ix_shifts_status", "shifts", ["status"])
        op.create_index("ix_shifts_deleted_at", "shifts", ["deleted_at"])
    if "employee_shift_assignments" not in inspector.get_table_names():
        op.create_table(
            "employee_shift_assignments", sa.Column("id", BIGINT, primary_key=True, autoincrement=True),
            sa.Column("employee_id", BIGINT, sa.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False),
            sa.Column("shift_id", BIGINT, sa.ForeignKey("shifts.id", ondelete="RESTRICT"), nullable=False),
            sa.Column("effective_from", sa.Date(), nullable=False), sa.Column("effective_to", sa.Date()),
            sa.Column("is_active", sa.Boolean(), nullable=False), *timestamps(), **TABLE_OPTIONS,
        )
        op.create_index("ix_shift_assignments_employee_id", "employee_shift_assignments", ["employee_id"])
        op.create_index("ix_shift_assignments_shift_id", "employee_shift_assignments", ["shift_id"])
        op.create_index("ix_shift_assignments_is_active", "employee_shift_assignments", ["is_active"])
    if "shift_requests" not in inspector.get_table_names():
        op.create_table(
            "shift_requests", sa.Column("id", BIGINT, primary_key=True, autoincrement=True),
            sa.Column("request_type", sa.String(20), nullable=False), sa.Column("request_date", sa.Date(), nullable=False),
            sa.Column("requester_id", BIGINT, sa.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False),
            sa.Column("current_shift_id", BIGINT, sa.ForeignKey("shifts.id", ondelete="RESTRICT"), nullable=False),
            sa.Column("target_employee_id", BIGINT, sa.ForeignKey("employees.id", ondelete="SET NULL")),
            sa.Column("new_shift_id", BIGINT, sa.ForeignKey("shifts.id", ondelete="SET NULL")),
            sa.Column("remarks", sa.Text()), sa.Column("status", sa.String(20), nullable=False),
            sa.Column("reviewed_by", BIGINT, sa.ForeignKey("users.id", ondelete="SET NULL")),
            sa.Column("reviewed_at", sa.DateTime()), *timestamps(), **TABLE_OPTIONS,
        )
        op.create_index("ix_shift_requests_status", "shift_requests", ["status"])
        op.create_index("ix_shift_requests_requester_id", "shift_requests", ["requester_id"])


def downgrade():
    op.drop_table("shift_requests")
    op.drop_table("employee_shift_assignments")
    op.drop_table("shifts")
