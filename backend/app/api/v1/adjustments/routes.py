from datetime import date
from flask import Blueprint,request
from flask_jwt_extended import get_jwt_identity
from app.api.v1.adjustments.service import create_adjustment,get_adjustments
from app.api.v1.adjustments.validators import validate_entry
from app.common.decorators import roles_required
from app.common.responses import error_response,success_response
adjustments_bp=Blueprint("adjustments",__name__)
@adjustments_bp.get("/")
@roles_required("Super Admin","HR Manager","Department Manager")
def entries():
    month=(request.args.get("month")or date.today().strftime("%Y-%m")).strip()
    try:data=get_adjustments(month,(request.args.get("search")or"").strip(),(request.args.get("type")or"").strip(),(request.args.get("status")or"").strip())
    except ValueError:return error_response("Month must use YYYY-MM format.",422)
    return success_response(data,"Adjustments loaded")
@adjustments_bp.post("/")
@roles_required("Super Admin","HR Manager")
def add_entry():
    validation=validate_entry(request.get_json(silent=True)or{})
    if not validation["is_valid"]:return error_response("Invalid adjustment data.",422,validation["errors"])
    item,errors=create_adjustment(validation["data"],validation["category"],validation["kind"],int(get_jwt_identity()))
    if errors:return error_response("Unable to create adjustment.",422,errors)
    return success_response(item,"Adjustment created",201)
