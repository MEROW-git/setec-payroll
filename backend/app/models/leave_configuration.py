from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


leave_group_types = db.Table(
    "leave_group_types",
    db.Column("group_id", UnsignedBigInteger, db.ForeignKey("leave_groups.id", ondelete="CASCADE"), primary_key=True),
    db.Column("leave_type_id", UnsignedBigInteger, db.ForeignKey("leave_types.id", ondelete="CASCADE"), primary_key=True),
)


class LeaveYear(BaseModel, SoftDeleteMixin):
    __tablename__ = "leave_years"
    year = db.Column(db.Integer, unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="active")


class LeaveGroup(BaseModel, SoftDeleteMixin):
    __tablename__ = "leave_groups"
    name = db.Column(db.String(150), unique=True, nullable=False)
    leave_types = db.relationship("LeaveType", secondary=leave_group_types)


class LeavePolicy(BaseModel, SoftDeleteMixin):
    __tablename__ = "leave_policies"
    name = db.Column(db.String(150), unique=True, nullable=False)
    count_type = db.Column(db.String(30), nullable=False, default="daily")
    considerable_hours = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    adjusted_days = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
