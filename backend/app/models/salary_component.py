from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin


class SalaryComponent(BaseModel, SoftDeleteMixin):
    __tablename__ = "salary_components"
    __table_args__ = (
        db.CheckConstraint("default_amount >= 0", name="ck_salary_components_default_amount_nonnegative"),
        db.Index("ix_salary_components_component_type", "component_type"),
        db.Index("ix_salary_components_is_active", "is_active"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    name = db.Column(db.String(150), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    component_type = db.Column(db.String(30), nullable=False)
    calculation_type = db.Column(db.String(30), default="fixed", nullable=False)
    default_amount = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    is_taxable = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    description = db.Column(db.Text)

    employee_components = db.relationship("EmployeeSalaryComponent", back_populates="salary_component")
