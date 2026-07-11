from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class Department(BaseModel, SoftDeleteMixin):
    __tablename__ = "departments"
    __table_args__ = (
        db.Index("ix_departments_manager_employee_id", "manager_employee_id"),
        db.Index("ix_departments_is_active", "is_active"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    name = db.Column(db.String(150), unique=True, nullable=False)
    code = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text)
    annual_budget = db.Column(db.Numeric(14, 2))
    manager_employee_id = db.Column(
        UnsignedBigInteger,
        db.ForeignKey("employees.id", ondelete="SET NULL", use_alter=True, name="fk_departments_manager_employee_id"),
        nullable=True,
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    manager = db.relationship("Employee", foreign_keys=[manager_employee_id], post_update=True)
    positions = db.relationship("Position", back_populates="department")
    employees = db.relationship(
        "Employee",
        foreign_keys="Employee.department_id",
        back_populates="department",
    )
    announcements = db.relationship("Announcement", back_populates="department")
    job_openings = db.relationship("JobOpening", back_populates="department")
