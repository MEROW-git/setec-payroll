"""Add leave configuration management."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


revision = "0005_leave"
down_revision = "0004_shifts"
branch_labels = None
depends_on = None
BIGINT = mysql.BIGINT(unsigned=True)
OPTIONS = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"}


def stamps(soft=True):
    values = [sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False)]
    if soft: values.append(sa.Column("deleted_at", sa.DateTime()))
    return values


def upgrade():
    inspector = sa.inspect(op.get_bind())
    type_columns = {column["name"] for column in inspector.get_columns("leave_types")}
    if "count_type" not in type_columns: op.add_column("leave_types", sa.Column("count_type", sa.String(30), nullable=False, server_default="daily"))
    if "special_types" not in type_columns: op.add_column("leave_types", sa.Column("special_types", sa.JSON()))
    holiday_columns = {column["name"] for column in inspector.get_columns("holidays")}
    if "end_date" not in holiday_columns: op.add_column("holidays", sa.Column("end_date", sa.Date()))
    if "department_id" not in holiday_columns:
        op.add_column("holidays", sa.Column("department_id", BIGINT))
        op.create_foreign_key("fk_holidays_department_id", "holidays", "departments", ["department_id"], ["id"], ondelete="SET NULL")
    tables = inspector.get_table_names()
    if "leave_years" not in tables:
        op.create_table("leave_years", sa.Column("id", BIGINT, primary_key=True, autoincrement=True), sa.Column("year", sa.Integer(), nullable=False, unique=True), sa.Column("start_date", sa.Date(), nullable=False), sa.Column("end_date", sa.Date(), nullable=False), sa.Column("status", sa.String(20), nullable=False), *stamps(), **OPTIONS)
    if "leave_groups" not in tables:
        op.create_table("leave_groups", sa.Column("id", BIGINT, primary_key=True, autoincrement=True), sa.Column("name", sa.String(150), nullable=False, unique=True), *stamps(), **OPTIONS)
    if "leave_group_types" not in tables:
        op.create_table("leave_group_types", sa.Column("group_id", BIGINT, sa.ForeignKey("leave_groups.id", ondelete="CASCADE"), primary_key=True), sa.Column("leave_type_id", BIGINT, sa.ForeignKey("leave_types.id", ondelete="CASCADE"), primary_key=True), **OPTIONS)
    if "leave_policies" not in tables:
        op.create_table("leave_policies", sa.Column("id", BIGINT, primary_key=True, autoincrement=True), sa.Column("name", sa.String(150), nullable=False, unique=True), sa.Column("count_type", sa.String(30), nullable=False), sa.Column("considerable_hours", sa.Numeric(8,2), nullable=False), sa.Column("adjusted_days", sa.Numeric(8,2), nullable=False), sa.Column("description", sa.Text()), sa.Column("is_active", sa.Boolean(), nullable=False), *stamps(), **OPTIONS)


def downgrade():
    op.drop_table("leave_policies"); op.drop_table("leave_group_types"); op.drop_table("leave_groups"); op.drop_table("leave_years")
    op.drop_constraint("fk_holidays_department_id", "holidays", type_="foreignkey"); op.drop_column("holidays", "department_id"); op.drop_column("holidays", "end_date")
    op.drop_column("leave_types", "special_types"); op.drop_column("leave_types", "count_type")
