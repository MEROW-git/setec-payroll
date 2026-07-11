from app.extensions import db
from app.models.base import BaseModel, UnsignedBigInteger


class Holiday(BaseModel):
    __tablename__ = "holidays"
    __table_args__ = (
        db.UniqueConstraint("holiday_date", name="uq_holidays_holiday_date"),
        db.Index("ix_holidays_holiday_date", "holiday_date"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    name = db.Column(db.String(200), nullable=False)
    holiday_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    department_id = db.Column(UnsignedBigInteger, db.ForeignKey("departments.id", ondelete="SET NULL"))
    is_paid = db.Column(db.Boolean, default=True, nullable=False)
    description = db.Column(db.Text)

    department = db.relationship("Department")
