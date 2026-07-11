"""Add department budgets and position permissions."""

from alembic import op
import sqlalchemy as sa


revision = "0002_budget_permissions"
down_revision = "0001_initial_hrm_schema"
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    department_columns = {column["name"] for column in inspector.get_columns("departments")}
    position_columns = {column["name"] for column in inspector.get_columns("positions")}

    if "annual_budget" not in department_columns:
        op.add_column("departments", sa.Column("annual_budget", sa.Numeric(14, 2), nullable=True))
    if "permissions" not in position_columns:
        op.add_column("positions", sa.Column("permissions", sa.JSON(), nullable=True))


def downgrade():
    op.drop_column("positions", "permissions")
    op.drop_column("departments", "annual_budget")
