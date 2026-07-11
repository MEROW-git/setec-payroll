from datetime import datetime,timezone
from app.models import Announcement,Event,EventType
from app.api.v1.events.repository import get_type,list_events,list_notices,list_types,save
from app.api.v1.events.schemas import event_data,notice_data,type_data
def get_events(search=""):return[event_data(x)for x in list_events(search)]
def get_notices(search=""):return[notice_data(x)for x in list_notices(search)]
def get_types():return[type_data(x)for x in list_types()]
def create_event(data,user_id):
 if not get_type(data["event_type_id"]):return None,{"event_type_id":["Event type was not found."]}
 data["created_by"]=user_id;item=save(Event(**data));item.event_type=get_type(item.event_type_id);return event_data(item),None
def create_notice(data,user_id):
 published_at=datetime.combine(data.pop("notice_date"),datetime.min.time(),tzinfo=timezone.utc);item=save(Announcement(**data,published_by=user_id,published_at=published_at));return notice_data(item),None
def create_type(name):
 if any(x.name.lower()==name.lower()for x in list_types()):return None,{"name":["Event type already exists."]}
 return type_data(save(EventType(name=name,color="indigo"))),None
