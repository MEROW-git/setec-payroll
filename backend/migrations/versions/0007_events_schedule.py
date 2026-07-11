"""Add events schedule and notice priority."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
revision="0007_events";down_revision="0006_adjustments";branch_labels=None;depends_on=None
BIGINT=mysql.BIGINT(unsigned=True);OPTIONS={"mysql_charset":"utf8mb4","mysql_collate":"utf8mb4_unicode_ci"}
def stamps():return[sa.Column("created_at",sa.DateTime(),nullable=False),sa.Column("updated_at",sa.DateTime(),nullable=False),sa.Column("deleted_at",sa.DateTime())]
def upgrade():
    inspector=sa.inspect(op.get_bind());columns={x["name"]for x in inspector.get_columns("announcements")}
    if"priority"not in columns:op.add_column("announcements",sa.Column("priority",sa.String(20),nullable=False,server_default="medium"))
    tables=inspector.get_table_names()
    if"event_types"not in tables:
        op.create_table("event_types",sa.Column("id",BIGINT,primary_key=True,autoincrement=True),sa.Column("name",sa.String(100),nullable=False,unique=True),sa.Column("color",sa.String(30),nullable=False),*stamps(),**OPTIONS)
    if"events"not in tables:
        op.create_table("events",sa.Column("id",BIGINT,primary_key=True,autoincrement=True),sa.Column("title",sa.String(200),nullable=False),sa.Column("event_type_id",BIGINT,sa.ForeignKey("event_types.id",ondelete="RESTRICT"),nullable=False),sa.Column("event_date",sa.Date(),nullable=False),sa.Column("start_time",sa.Time()),sa.Column("end_time",sa.Time()),sa.Column("is_all_day",sa.Boolean(),nullable=False),sa.Column("location",sa.String(255),nullable=False),sa.Column("audience_type",sa.String(30),nullable=False),sa.Column("department_id",BIGINT,sa.ForeignKey("departments.id",ondelete="SET NULL")),sa.Column("description",sa.Text()),sa.Column("status",sa.String(20),nullable=False),sa.Column("created_by",BIGINT,sa.ForeignKey("users.id",ondelete="SET NULL")),*stamps(),**OPTIONS)
        op.create_index("ix_events_event_date","events",["event_date"]);op.create_index("ix_events_status","events",["status"])
    bind=op.get_bind();count=bind.execute(sa.text("SELECT COUNT(*) FROM event_types")).scalar()
    if not count:
        bind.execute(sa.text("INSERT INTO event_types (name,color,created_at,updated_at) VALUES ('Meeting','violet',NOW(),NOW()),('Deadline','rose',NOW(),NOW()),('Holiday','blue',NOW(),NOW()),('Workshop','slate',NOW(),NOW())"))
def downgrade():
    op.drop_table("events");op.drop_table("event_types");op.drop_column("announcements","priority")
