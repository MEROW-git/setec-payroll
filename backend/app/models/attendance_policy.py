from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin


class AttendancePolicy(BaseModel, SoftDeleteMixin):
    __tablename__ = "attendance_policies"
    __table_args__ = (
        db.Index("ix_attendance_policies_is_active", "is_active"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    name = db.Column(db.String(150), unique=True, nullable=False)
    count_type = db.Column(db.String(30), nullable=False, default="daily")
    considerable_value = db.Column(db.Integer, nullable=False, default=0)
    adjusted_days = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
