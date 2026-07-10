from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class Announcement(BaseModel, SoftDeleteMixin):
    __tablename__ = "announcements"
    __table_args__ = (
        db.Index("ix_announcements_department_id", "department_id"),
        db.Index("ix_announcements_status", "status"),
        db.Index("ix_announcements_published_at", "published_at"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    audience_type = db.Column(db.String(30), default="all", nullable=False)
    department_id = db.Column(UnsignedBigInteger, db.ForeignKey("departments.id", ondelete="SET NULL"))
    published_by = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    published_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    status = db.Column(db.String(30), default="draft", nullable=False)

    department = db.relationship("Department", back_populates="announcements")
    publisher = db.relationship("User", back_populates="announcements")
