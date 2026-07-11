from flask import Blueprint,request
from flask_jwt_extended import get_jwt_identity
from app.api.v1.leave.service import configuration_summary,create_config,create_leave,dashboard,list_config,review_leave
from app.api.v1.leave.validators import config_payload,request_payload
from app.common.decorators import roles_required
from app.common.responses import error_response,success_response

leave_bp=Blueprint("leave",__name__)

@leave_bp.get("/")
@roles_required("Super Admin","HR Manager","Department Manager")
def requests():return success_response(dashboard((request.args.get("search")or"").strip()),"Leave requests loaded")

@leave_bp.post("/")
@roles_required("Super Admin","HR Manager","Department Manager")
def apply_leave():
    validation=request_payload(request.get_json(silent=True)or{})
    if not validation["is_valid"]:return error_response("Invalid leave request.",422,validation["errors"])
    item,errors=create_leave(validation["data"])
    if errors:return error_response("Unable to create leave request.",422,errors)
    return success_response(item,"Leave request created",201)

@leave_bp.patch("/<int:item_id>")
@roles_required("Super Admin","HR Manager")
def review(item_id):
    payload=request.get_json(silent=True)or{};status=payload.get("status")
    if status not in{"approved","rejected"}:return error_response("Review status is invalid.",422)
    item,errors=review_leave(item_id,status,int(get_jwt_identity()),payload.get("note"))
    if errors:return error_response("Unable to review leave request.",422,errors)
    return success_response(item,"Leave request reviewed")

@leave_bp.get("/settings/summary")
@roles_required("Super Admin","HR Manager")
def summary():return success_response(configuration_summary(),"Leave settings loaded")

@leave_bp.get("/config/<kind>")
@roles_required("Super Admin","HR Manager","Department Manager")
def config_list(kind):
    if kind not in{"types","years","groups","policies","holidays"}:return error_response("Configuration type not found.",404)
    return success_response(list_config(kind),f"Leave {kind} loaded")

@leave_bp.post("/config/<kind>")
@roles_required("Super Admin","HR Manager")
def config_create(kind):
    if kind not in{"types","years","groups","policies","holidays"}:return error_response("Configuration type not found.",404)
    validation=config_payload(kind,request.get_json(silent=True)or{})
    if not validation["is_valid"]:return error_response("Invalid configuration data.",422,validation["errors"])
    item,errors=create_config(kind,validation["data"])
    if errors:return error_response("Unable to create configuration.",409,errors)
    return success_response(item,"Leave configuration created",201)
