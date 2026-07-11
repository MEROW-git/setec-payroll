"""Add payroll adjustment status and creator."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = "0006_adjustments"
down_revision = "0005_leave"
branch_labels = None
depends_on = None
BIGINT = mysql.BIGINT(unsigned=True)


def upgrade():
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("employee_salary_components")}
    if "status" not in columns:
        op.add_column("employee_salary_components", sa.Column("status", sa.String(20), nullable=False, server_default="approved"))
    if "created_by" not in columns:
        op.add_column("employee_salary_components", sa.Column("created_by", BIGINT))
        op.create_foreign_key("fk_employee_components_created_by", "employee_salary_components", "users", ["created_by"], ["id"], ondelete="SET NULL")


def downgrade():
    op.drop_constraint("fk_employee_components_created_by", "employee_salary_components", type_="foreignkey")
    op.drop_column("employee_salary_components", "created_by")
    op.drop_column("employee_salary_components", "status")
