from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class Position(BaseModel, SoftDeleteMixin):
    __tablename__ = "positions"
    __table_args__ = (
        db.UniqueConstraint("department_id", "title", name="uq_positions_department_title"),
        db.CheckConstraint("min_salary IS NULL OR max_salary IS NULL OR min_salary <= max_salary", name="ck_positions_salary_range"),
        db.Index("ix_positions_department_id", "department_id"),
        db.Index("ix_positions_is_active", "is_active"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    department_id = db.Column(UnsignedBigInteger, db.ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    permissions = db.Column(db.JSON)
    min_salary = db.Column(db.Numeric(12, 2))
    max_salary = db.Column(db.Numeric(12, 2))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    department = db.relationship("Department", back_populates="positions")
    employees = db.relationship("Employee", back_populates="position")
    job_openings = db.relationship("JobOpening", back_populates="position")
