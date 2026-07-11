from flask import Blueprint,request
from flask_jwt_extended import get_jwt_identity
from app.api.v1.events.service import create_event,create_notice,create_type,get_events,get_notices,get_types
from app.api.v1.events.validators import event_payload,notice_payload
from app.common.decorators import roles_required
from app.common.responses import error_response,success_response
events_bp=Blueprint("events",__name__)
@events_bp.get("/")
@roles_required("Super Admin","HR Manager","Department Manager","Employee")
def events():return success_response(get_events((request.args.get("search")or"").strip()),"Events loaded")
@events_bp.post("/")
@roles_required("Super Admin","HR Manager")
def add_event():
 validation=event_payload(request.get_json(silent=True)or{})
 if not validation["is_valid"]:return error_response("Invalid event data.",422,validation["errors"])
 item,errors=create_event(validation["data"],int(get_jwt_identity()))
 if errors:return error_response("Unable to create event.",422,errors)
 return success_response(item,"Event created",201)
@events_bp.get("/notices")
@roles_required("Super Admin","HR Manager","Department Manager","Employee")
def notices():return success_response(get_notices((request.args.get("search")or"").strip()),"Notices loaded")
@events_bp.post("/notices")
@roles_required("Super Admin","HR Manager")
def add_notice():
 validation=notice_payload(request.get_json(silent=True)or{})
 if not validation["is_valid"]:return error_response("Invalid notice data.",422,validation["errors"])
 return success_response(create_notice(validation["data"],int(get_jwt_identity()))[0],"Notice posted",201)
@events_bp.get("/types")
@roles_required("Super Admin","HR Manager","Department Manager")
def types():return success_response(get_types(),"Event types loaded")
@events_bp.post("/types")
@roles_required("Super Admin","HR Manager")
def add_type():
 name=((request.get_json(silent=True)or{}).get("name")or"").strip()
 if not name:return error_response("Event type name is required.",422)
 item,errors=create_type(name)
 if errors:return error_response("Unable to create event type.",409,errors)
 return success_response(item,"Event type created",201)
