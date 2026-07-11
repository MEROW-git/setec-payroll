from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class User(BaseModel, SoftDeleteMixin):
    __tablename__ = "users"
    __table_args__ = (
        db.Index("ix_users_role_id", "role_id"),
        db.Index("ix_users_email", "email"),
        db.Index("ix_users_is_active", "is_active"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    role_id = db.Column(UnsignedBigInteger, db.ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(191), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login_at = db.Column(db.DateTime)

    role = db.relationship("Role", back_populates="users")
    employee = db.relationship("Employee", back_populates="user", uselist=False)
    uploaded_documents = db.relationship("EmployeeDocument", back_populates="uploader")
    approved_attendance = db.relationship("Attendance", back_populates="approver")
    reviewed_leave_requests = db.relationship("LeaveRequest", back_populates="reviewer")
    created_payroll_periods = db.relationship(
        "PayrollPeriod",
        foreign_keys="PayrollPeriod.created_by",
        back_populates="creator",
    )
    finalized_payroll_periods = db.relationship(
        "PayrollPeriod",
        foreign_keys="PayrollPeriod.finalized_by",
        back_populates="finalizer",
    )
    announcements = db.relationship("Announcement", back_populates="publisher")
    job_openings = db.relationship("JobOpening", back_populates="creator")
    audit_logs = db.relationship("AuditLog", back_populates="user")
    preference = db.relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
