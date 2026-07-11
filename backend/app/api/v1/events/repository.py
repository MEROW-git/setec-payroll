from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.models import Announcement,Event,EventType
def list_events(search=""):
 q=Event.query.options(joinedload(Event.event_type),joinedload(Event.department)).filter(Event.deleted_at.is_(None))
 if search:q=q.filter(or_(Event.title.ilike(f"%{search}%"),Event.location.ilike(f"%{search}%")))
 return q.order_by(Event.event_date.asc()).all()
def list_notices(search=""):
 q=Announcement.query.options(joinedload(Announcement.department)).filter(Announcement.deleted_at.is_(None))
 if search:q=q.filter(or_(Announcement.title.ilike(f"%{search}%"),Announcement.content.ilike(f"%{search}%")))
 return q.order_by(Announcement.published_at.desc()).all()
def list_types():return EventType.query.filter(EventType.deleted_at.is_(None)).order_by(EventType.name).all()
def get_type(item_id):return EventType.query.filter(EventType.id==item_id,EventType.deleted_at.is_(None)).first()
def save(item):db.session.add(item);db.session.commit();return item
