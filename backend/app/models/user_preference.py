from app.extensions import db
from app.models.base import BaseModel, UnsignedBigInteger


class UserPreference(BaseModel):
    __tablename__ = "user_preferences"
    __table_args__ = ({"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},)

    user_id = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    theme = db.Column(db.String(20), default="system", nullable=False)
    density = db.Column(db.String(20), default="comfortable", nullable=False)
    email_notifications = db.Column(db.Boolean, default=True, nullable=False)
    push_notifications = db.Column(db.Boolean, default=True, nullable=False)
    leave_notifications = db.Column(db.Boolean, default=True, nullable=False)
    payroll_notifications = db.Column(db.Boolean, default=True, nullable=False)

    user = db.relationship("User", back_populates="preference")
