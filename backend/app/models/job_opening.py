from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class JobOpening(BaseModel, SoftDeleteMixin):
    __tablename__ = "job_openings"
    __table_args__ = (
        db.CheckConstraint("min_salary IS NULL OR max_salary IS NULL OR min_salary <= max_salary", name="ck_job_openings_salary_range"),
        db.Index("ix_job_openings_department_id", "department_id"),
        db.Index("ix_job_openings_position_id", "position_id"),
        db.Index("ix_job_openings_status", "status"),
        db.Index("ix_job_openings_closing_date", "closing_date"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    department_id = db.Column(UnsignedBigInteger, db.ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False)
    position_id = db.Column(UnsignedBigInteger, db.ForeignKey("positions.id", ondelete="SET NULL"))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    employment_type = db.Column(db.String(30), default="full_time", nullable=False)
    location = db.Column(db.String(200))
    min_salary = db.Column(db.Numeric(12, 2))
    max_salary = db.Column(db.Numeric(12, 2))
    openings_count = db.Column(db.Integer, default=1, nullable=False)
    closing_date = db.Column(db.Date)
    status = db.Column(db.String(30), default="draft", nullable=False)
    created_by = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="SET NULL"))

    department = db.relationship("Department", back_populates="job_openings")
    position = db.relationship("Position", back_populates="job_openings")
    creator = db.relationship("User", back_populates="job_openings")
    candidates = db.relationship("Candidate", back_populates="job_opening", cascade="all, delete-orphan")
