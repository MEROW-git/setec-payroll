"""Add per-user settings preferences."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = "0009_preferences"
down_revision = "0008_payroll"
branch_labels = None
depends_on = None
BIGINT = mysql.BIGINT(unsigned=True)
OPTIONS = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"}


def upgrade():
    if "user_preferences" not in sa.inspect(op.get_bind()).get_table_names():
        op.create_table(
            "user_preferences",
            sa.Column("id", BIGINT, primary_key=True, autoincrement=True),
            sa.Column("user_id", BIGINT, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
            sa.Column("theme", sa.String(20), nullable=False, server_default="system"),
            sa.Column("density", sa.String(20), nullable=False, server_default="comfortable"),
            sa.Column("email_notifications", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("push_notifications", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("leave_notifications", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("payroll_notifications", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            **OPTIONS,
        )


def downgrade():
    op.drop_table("user_preferences")
