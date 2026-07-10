from app.extensions import db
from app.models.base import BaseModel, UnsignedBigInteger


class Payroll(BaseModel):
    __tablename__ = "payrolls"
    __table_args__ = (
        db.UniqueConstraint("payroll_period_id", "employee_id", name="uq_payrolls_period_employee"),
        db.CheckConstraint("basic_salary >= 0", name="ck_payrolls_basic_salary_nonnegative"),
        db.CheckConstraint("total_allowance >= 0", name="ck_payrolls_total_allowance_nonnegative"),
        db.CheckConstraint("overtime_pay >= 0", name="ck_payrolls_overtime_pay_nonnegative"),
        db.CheckConstraint("bonus >= 0", name="ck_payrolls_bonus_nonnegative"),
        db.CheckConstraint("gross_salary >= 0", name="ck_payrolls_gross_salary_nonnegative"),
        db.CheckConstraint("total_deduction >= 0", name="ck_payrolls_total_deduction_nonnegative"),
        db.CheckConstraint("tax_amount >= 0", name="ck_payrolls_tax_amount_nonnegative"),
        db.CheckConstraint("net_salary >= 0", name="ck_payrolls_net_salary_nonnegative"),
        db.Index("ix_payrolls_employee_id", "employee_id"),
        db.Index("ix_payrolls_payroll_period_id", "payroll_period_id"),
        db.Index("ix_payrolls_payment_status", "payment_status"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    payroll_period_id = db.Column(UnsignedBigInteger, db.ForeignKey("payroll_periods.id", ondelete="CASCADE"), nullable=False)
    employee_id = db.Column(UnsignedBigInteger, db.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    basic_salary = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    total_allowance = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    overtime_pay = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    bonus = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    gross_salary = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    total_deduction = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    tax_amount = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    net_salary = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    payment_status = db.Column(db.String(30), default="unpaid", nullable=False)
    paid_at = db.Column(db.DateTime)
    payment_reference = db.Column(db.String(150))
    note = db.Column(db.Text)

    payroll_period = db.relationship("PayrollPeriod", back_populates="payrolls")
    employee = db.relationship("Employee", back_populates="payrolls")
