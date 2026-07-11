from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class EmployeeSalaryComponent(BaseModel, SoftDeleteMixin):
    __tablename__ = "employee_salary_components"
    __table_args__ = (
        db.CheckConstraint("amount >= 0", name="ck_employee_salary_components_amount_nonnegative"),
        db.Index("ix_employee_salary_components_employee_id", "employee_id"),
        db.Index("ix_employee_salary_components_salary_component_id", "salary_component_id"),
        db.Index("ix_employee_salary_components_effective_date", "effective_date"),
        db.Index("ix_employee_salary_components_is_active", "is_active"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    employee_id = db.Column(UnsignedBigInteger, db.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    salary_component_id = db.Column(
        UnsignedBigInteger,
        db.ForeignKey("salary_components.id", ondelete="RESTRICT"),
        nullable=False,
    )
    amount = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    status = db.Column(db.String(20), default="approved", nullable=False)
    created_by = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="SET NULL"))

    employee = db.relationship("Employee", back_populates="salary_components")
    salary_component = db.relationship("SalaryComponent", back_populates="employee_components")
    creator = db.relationship("User")
