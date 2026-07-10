from app.extensions import db
from app.models.base import BaseModel, UnsignedBigInteger


class PayrollPeriod(BaseModel):
    __tablename__ = "payroll_periods"
    __table_args__ = (
        db.UniqueConstraint("start_date", "end_date", name="uq_payroll_periods_start_end"),
        db.CheckConstraint("end_date >= start_date", name="ck_payroll_periods_date_range"),
        db.Index("ix_payroll_periods_status", "status"),
        db.Index("ix_payroll_periods_start_date", "start_date"),
        db.Index("ix_payroll_periods_end_date", "end_date"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    pay_date = db.Column(db.Date)
    status = db.Column(db.String(30), default="draft", nullable=False)
    created_by = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="SET NULL"))
    finalized_by = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="SET NULL"))
    finalized_at = db.Column(db.DateTime)

    creator = db.relationship("User", foreign_keys=[created_by], back_populates="created_payroll_periods")
    finalizer = db.relationship("User", foreign_keys=[finalized_by], back_populates="finalized_payroll_periods")
    payrolls = db.relationship("Payroll", back_populates="payroll_period", cascade="all, delete-orphan")
