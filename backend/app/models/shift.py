from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class Shift(BaseModel, SoftDeleteMixin):
    __tablename__ = "shifts"
    __table_args__ = (
        db.Index("ix_shifts_status", "status"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    name = db.Column(db.String(150), unique=True, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    shift_type = db.Column(db.String(30), nullable=False, default="regular")
    status = db.Column(db.String(20), nullable=False, default="active")
    notes = db.Column(db.Text)

    assignments = db.relationship("EmployeeShiftAssignment", back_populates="shift")
    current_requests = db.relationship("ShiftRequest", foreign_keys="ShiftRequest.current_shift_id", back_populates="current_shift")
    requested_requests = db.relationship("ShiftRequest", foreign_keys="ShiftRequest.new_shift_id", back_populates="new_shift")


class EmployeeShiftAssignment(BaseModel):
    __tablename__ = "employee_shift_assignments"
    __table_args__ = (
        db.Index("ix_shift_assignments_employee_id", "employee_id"),
        db.Index("ix_shift_assignments_shift_id", "shift_id"),
        db.Index("ix_shift_assignments_is_active", "is_active"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    employee_id = db.Column(UnsignedBigInteger, db.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    shift_id = db.Column(UnsignedBigInteger, db.ForeignKey("shifts.id", ondelete="RESTRICT"), nullable=False)
    effective_from = db.Column(db.Date, nullable=False)
    effective_to = db.Column(db.Date)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    employee = db.relationship("Employee")
    shift = db.relationship("Shift", back_populates="assignments")


class ShiftRequest(BaseModel):
    __tablename__ = "shift_requests"
    __table_args__ = (
        db.Index("ix_shift_requests_status", "status"),
        db.Index("ix_shift_requests_requester_id", "requester_id"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    request_type = db.Column(db.String(20), nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    requester_id = db.Column(UnsignedBigInteger, db.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    current_shift_id = db.Column(UnsignedBigInteger, db.ForeignKey("shifts.id", ondelete="RESTRICT"), nullable=False)
    target_employee_id = db.Column(UnsignedBigInteger, db.ForeignKey("employees.id", ondelete="SET NULL"))
    new_shift_id = db.Column(UnsignedBigInteger, db.ForeignKey("shifts.id", ondelete="SET NULL"))
    remarks = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default="pending")
    reviewed_by = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="SET NULL"))
    reviewed_at = db.Column(db.DateTime)

    requester = db.relationship("Employee", foreign_keys=[requester_id])
    target_employee = db.relationship("Employee", foreign_keys=[target_employee_id])
    current_shift = db.relationship("Shift", foreign_keys=[current_shift_id], back_populates="current_requests")
    new_shift = db.relationship("Shift", foreign_keys=[new_shift_id], back_populates="requested_requests")
    reviewer = db.relationship("User")
