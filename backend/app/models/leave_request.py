from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class LeaveRequest(BaseModel, SoftDeleteMixin):
    __tablename__ = "leave_requests"
    __table_args__ = (
        db.CheckConstraint("end_date >= start_date", name="ck_leave_requests_date_range"),
        db.CheckConstraint("total_days > 0", name="ck_leave_requests_total_days_positive"),
        db.Index("ix_leave_requests_employee_id", "employee_id"),
        db.Index("ix_leave_requests_leave_type_id", "leave_type_id"),
        db.Index("ix_leave_requests_status", "status"),
        db.Index("ix_leave_requests_start_date", "start_date"),
        db.Index("ix_leave_requests_end_date", "end_date"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    employee_id = db.Column(UnsignedBigInteger, db.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    leave_type_id = db.Column(UnsignedBigInteger, db.ForeignKey("leave_types.id", ondelete="RESTRICT"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Numeric(5, 2), nullable=False)
    reason = db.Column(db.Text)
    attachment_path = db.Column(db.String(500))
    status = db.Column(db.String(30), default="pending", nullable=False)
    reviewed_by = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="SET NULL"))
    reviewed_at = db.Column(db.DateTime)
    reviewer_note = db.Column(db.Text)

    employee = db.relationship("Employee", back_populates="leave_requests")
    leave_type = db.relationship("LeaveType", back_populates="leave_requests")
    reviewer = db.relationship("User", back_populates="reviewed_leave_requests")
