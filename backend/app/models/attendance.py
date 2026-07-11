from app.extensions import db
from app.models.base import BaseModel, UnsignedBigInteger


class Attendance(BaseModel):
    __tablename__ = "attendance"
    __table_args__ = (
        db.UniqueConstraint("employee_id", "attendance_date", name="uq_attendance_employee_date"),
        db.CheckConstraint("work_minutes >= 0", name="ck_attendance_work_minutes_nonnegative"),
        db.CheckConstraint("overtime_minutes >= 0", name="ck_attendance_overtime_minutes_nonnegative"),
        db.Index("ix_attendance_attendance_date", "attendance_date"),
        db.Index("ix_attendance_employee_id", "employee_id"),
        db.Index("ix_attendance_status", "status"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    employee_id = db.Column(UnsignedBigInteger, db.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    work_minutes = db.Column(db.Integer, default=0, nullable=False)
    overtime_minutes = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(40), nullable=False, default="present")
    work_location = db.Column(db.String(100))
    note = db.Column(db.Text)
    approved_by = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="SET NULL"))

    employee = db.relationship("Employee", back_populates="attendance_records")
    approver = db.relationship("User", back_populates="approved_attendance")
