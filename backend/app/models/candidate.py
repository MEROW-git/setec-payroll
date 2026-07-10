from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class Candidate(BaseModel, SoftDeleteMixin):
    __tablename__ = "candidates"
    __table_args__ = (
        db.Index("ix_candidates_job_opening_id", "job_opening_id"),
        db.Index("ix_candidates_email", "email"),
        db.Index("ix_candidates_status", "status"),
        db.Index("ix_candidates_applied_at", "applied_at"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    job_opening_id = db.Column(UnsignedBigInteger, db.ForeignKey("job_openings.id", ondelete="CASCADE"), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(191))
    phone = db.Column(db.String(30))
    address = db.Column(db.Text)
    cv_file_path = db.Column(db.String(500))
    cover_letter = db.Column(db.Text)
    years_experience = db.Column(db.Numeric(5, 2))
    expected_salary = db.Column(db.Numeric(12, 2))
    status = db.Column(db.String(30), default="applied", nullable=False)
    applied_at = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)

    job_opening = db.relationship("JobOpening", back_populates="candidates")
