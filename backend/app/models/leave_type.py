from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin


class LeaveType(BaseModel, SoftDeleteMixin):
    __tablename__ = "leave_types"
    __table_args__ = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"}

    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text)
    days_per_year = db.Column(db.Numeric(5, 2), default=0, nullable=False)
    is_paid = db.Column(db.Boolean, default=True, nullable=False)
    requires_attachment = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    leave_requests = db.relationship("LeaveRequest", back_populates="leave_type")
