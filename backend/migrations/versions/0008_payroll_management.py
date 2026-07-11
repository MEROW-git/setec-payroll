"""Add payroll configuration."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
revision="0008_payroll";down_revision="0007_events";branch_labels=None;depends_on=None
BIGINT=mysql.BIGINT(unsigned=True);OPTIONS={"mysql_charset":"utf8mb4","mysql_collate":"utf8mb4_unicode_ci"}
def stamps():return[sa.Column("created_at",sa.DateTime(),nullable=False),sa.Column("updated_at",sa.DateTime(),nullable=False),sa.Column("deleted_at",sa.DateTime())]
def upgrade():
 inspector=sa.inspect(op.get_bind());columns={x["name"]for x in inspector.get_columns("salary_components")}
 if"description"not in columns:op.add_column("salary_components",sa.Column("description",sa.Text()))
 tables=inspector.get_table_names()
 if"payroll_cycles"not in tables:op.create_table("payroll_cycles",sa.Column("id",BIGINT,primary_key=True,autoincrement=True),sa.Column("name",sa.String(150),nullable=False,unique=True),sa.Column("frequency",sa.String(30),nullable=False),sa.Column("pay_day",sa.Integer(),nullable=False),sa.Column("is_default",sa.Boolean(),nullable=False),sa.Column("is_active",sa.Boolean(),nullable=False),*stamps(),**OPTIONS)
 if"tax_rules"not in tables:op.create_table("tax_rules",sa.Column("id",BIGINT,primary_key=True,autoincrement=True),sa.Column("min_income",sa.Numeric(14,2),nullable=False),sa.Column("max_income",sa.Numeric(14,2)),sa.Column("rate",sa.Numeric(6,3),nullable=False),sa.Column("description",sa.Text()),sa.Column("is_active",sa.Boolean(),nullable=False),*stamps(),**OPTIONS)
 if"payroll_policies"not in tables:op.create_table("payroll_policies",sa.Column("id",BIGINT,primary_key=True,autoincrement=True),sa.Column("name",sa.String(150),nullable=False,unique=True),sa.Column("category",sa.String(30),nullable=False),sa.Column("count_type",sa.String(30),nullable=False),sa.Column("policy_type",sa.String(30),nullable=False),sa.Column("considerable_value",sa.Numeric(10,2),nullable=False),sa.Column("adjusted_value",sa.Numeric(12,2),nullable=False),sa.Column("value_mode",sa.String(20),nullable=False),sa.Column("description",sa.Text()),sa.Column("is_active",sa.Boolean(),nullable=False),*stamps(),**OPTIONS)
 if"payroll_settings"not in tables:op.create_table("payroll_settings",sa.Column("id",BIGINT,primary_key=True,autoincrement=True),sa.Column("setting_key",sa.String(100),nullable=False,unique=True),sa.Column("setting_value",sa.JSON(),nullable=False),sa.Column("created_at",sa.DateTime(),nullable=False),sa.Column("updated_at",sa.DateTime(),nullable=False),**OPTIONS)
 bind=op.get_bind();count=bind.execute(sa.text("SELECT COUNT(*) FROM payroll_cycles")).scalar()
 if not count:bind.execute(sa.text("INSERT INTO payroll_cycles(name,frequency,pay_day,is_default,is_active,created_at,updated_at)VALUES('Standard Monthly','monthly',30,1,1,NOW(),NOW())"))
def downgrade():
 op.drop_table("payroll_settings");op.drop_table("payroll_policies");op.drop_table("tax_rules");op.drop_table("payroll_cycles");op.drop_column("salary_components","description")
