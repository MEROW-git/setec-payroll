from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from app.api.v1.shifts.service import create_shift_record, create_shift_request, get_shift_management, get_shift_requests, review_request
from app.api.v1.shifts.validators import validate_request, validate_shift
from app.common.decorators import roles_required
from app.common.responses import error_response, success_response

shifts_bp = Blueprint("shifts", __name__)


@shifts_bp.get("/")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def shifts(): return success_response(get_shift_management((request.args.get("search") or "").strip()), "Shifts loaded")


@shifts_bp.post("/")
@roles_required("Super Admin", "HR Manager")
def add_shift():
    validation = validate_shift(request.get_json(silent=True) or {})
    if not validation["is_valid"]: return error_response("Invalid shift data.", 422, validation["errors"])
    item, errors = create_shift_record(validation["data"])
    if errors: return error_response("Unable to create shift.", 409, errors)
    return success_response(item, "Shift created", 201)


@shifts_bp.get("/requests")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def requests_list(): return success_response(get_shift_requests((request.args.get("search") or "").strip()), "Shift requests loaded")


@shifts_bp.post("/requests")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def add_request():
    validation = validate_request(request.get_json(silent=True) or {})
    if not validation["is_valid"]: return error_response("Invalid shift request.", 422, validation["errors"])
    item, errors = create_shift_request(validation["data"])
    if errors: return error_response("Unable to create shift request.", 422, errors)
    return success_response(item, "Shift request submitted", 201)


@shifts_bp.patch("/requests/<int:request_id>")
@roles_required("Super Admin", "HR Manager")
def update_request(request_id):
    item, errors = review_request(request_id, (request.get_json(silent=True) or {}).get("status"), int(get_jwt_identity()))
    if errors: return error_response("Unable to review shift request.", 422, errors)
    return success_response(item, "Shift request reviewed")
