from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class EventType(BaseModel, SoftDeleteMixin):
    __tablename__="event_types"
    name=db.Column(db.String(100),unique=True,nullable=False)
    color=db.Column(db.String(30),nullable=False,default="indigo")
    events=db.relationship("Event",back_populates="event_type")


class Event(BaseModel, SoftDeleteMixin):
    __tablename__="events"
    __table_args__=(db.Index("ix_events_event_date","event_date"),db.Index("ix_events_status","status"),{"mysql_charset":"utf8mb4","mysql_collate":"utf8mb4_unicode_ci"})
    title=db.Column(db.String(200),nullable=False)
    event_type_id=db.Column(UnsignedBigInteger,db.ForeignKey("event_types.id",ondelete="RESTRICT"),nullable=False)
    event_date=db.Column(db.Date,nullable=False)
    start_time=db.Column(db.Time)
    end_time=db.Column(db.Time)
    is_all_day=db.Column(db.Boolean,nullable=False,default=False)
    location=db.Column(db.String(255),nullable=False)
    audience_type=db.Column(db.String(30),nullable=False,default="all")
    department_id=db.Column(UnsignedBigInteger,db.ForeignKey("departments.id",ondelete="SET NULL"))
    description=db.Column(db.Text)
    status=db.Column(db.String(20),nullable=False,default="active")
    created_by=db.Column(UnsignedBigInteger,db.ForeignKey("users.id",ondelete="SET NULL"))
    event_type=db.relationship("EventType",back_populates="events")
    department=db.relationship("Department")
    creator=db.relationship("User")
