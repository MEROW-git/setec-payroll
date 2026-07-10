from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class PerformanceReview(BaseModel, SoftDeleteMixin):
    __tablename__ = "performance_reviews"
    __table_args__ = (
        db.Index("ix_performance_reviews_employee_id", "employee_id"),
        db.Index("ix_performance_reviews_reviewer_id", "reviewer_id"),
        db.Index("ix_performance_reviews_review_date", "review_date"),
        db.Index("ix_performance_reviews_status", "status"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    employee_id = db.Column(UnsignedBigInteger, db.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    reviewer_id = db.Column(UnsignedBigInteger, db.ForeignKey("employees.id", ondelete="RESTRICT"), nullable=False)
    review_date = db.Column(db.Date, nullable=False)
    review_period_start = db.Column(db.Date)
    review_period_end = db.Column(db.Date)
    score = db.Column(db.Numeric(5, 2))
    strengths = db.Column(db.Text)
    improvements = db.Column(db.Text)
    comments = db.Column(db.Text)
    status = db.Column(db.String(30), default="draft", nullable=False)

    employee = db.relationship("Employee", foreign_keys=[employee_id], back_populates="performance_reviews")
    reviewer = db.relationship("Employee", foreign_keys=[reviewer_id], back_populates="reviews_given")
