from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class EmployeeDocument(BaseModel, SoftDeleteMixin):
    __tablename__ = "employee_documents"
    __table_args__ = (
        db.Index("ix_employee_documents_employee_id", "employee_id"),
        db.Index("ix_employee_documents_document_type", "document_type"),
        db.Index("ix_employee_documents_expiry_date", "expiry_date"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    employee_id = db.Column(UnsignedBigInteger, db.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    document_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    issue_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    uploaded_by = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="SET NULL"))

    employee = db.relationship("Employee", back_populates="documents")
    uploader = db.relationship("User", back_populates="uploaded_documents")
