from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin


class Role(BaseModel, SoftDeleteMixin):
    __tablename__ = "roles"
    __table_args__ = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"}

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    users = db.relationship("User", back_populates="role")
