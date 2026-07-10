from app.extensions import db
from app.models.base import BaseModel, UnsignedBigInteger


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"
    __table_args__ = (
        db.Index("ix_audit_logs_user_id", "user_id"),
        db.Index("ix_audit_logs_entity_type", "entity_type"),
        db.Index("ix_audit_logs_entity_id", "entity_id"),
        db.Index("ix_audit_logs_action", "action"),
        db.Index("ix_audit_logs_created_at", "created_at"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    user_id = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="SET NULL"))
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(100), nullable=False)
    entity_id = db.Column(UnsignedBigInteger)
    old_values = db.Column(db.JSON)
    new_values = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))

    user = db.relationship("User", back_populates="audit_logs")
