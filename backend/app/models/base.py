from datetime import datetime, timezone

from sqlalchemy.dialects import mysql

from app.extensions import db

UnsignedBigInteger = db.BigInteger().with_variant(mysql.BIGINT(unsigned=True), "mysql")


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(UnsignedBigInteger, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self) -> dict:
        hidden = {"password_hash"}
        data = {}
        for column in self.__table__.columns:
            if column.name in hidden:
                continue
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            data[column.name] = value
        return data


class SoftDeleteMixin:
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)
