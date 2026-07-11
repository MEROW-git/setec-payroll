from flask import Blueprint, request

from app.api.v1.positions.service import (
    assign_position_to_employee,
    create_position_record,
    get_position_management,
    get_positions,
)
from app.api.v1.positions.validators import validate_create_position_payload, validate_position_assignment_payload
from app.common.decorators import roles_required
from app.common.responses import error_response, success_response

positions_bp = Blueprint("positions", __name__)


@positions_bp.get("/management")
@roles_required("Super Admin", "HR Manager")
def position_management():
    data = get_position_management(search=(request.args.get("search") or "").strip())
    return success_response(data=data, message="Employee roles loaded")


@positions_bp.get("/")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def list_positions():
    return success_response(
        data=get_positions(department_id=(request.args.get("department_id") or "").strip()),
        message="Positions loaded",
    )


@positions_bp.post("/")
@roles_required("Super Admin", "HR Manager")
def add_position():
    validation = validate_create_position_payload(request.get_json(silent=True) or {})
    if not validation["is_valid"]:
        return error_response("Invalid role data.", status_code=422, errors=validation["errors"])

    position, errors = create_position_record(validation["data"])
    if errors:
        return error_response("Unable to create role.", status_code=422, errors=errors)

    return success_response(data=position, message="Employee role created", status_code=201)


@positions_bp.post("/<int:position_id>/assign")
@roles_required("Super Admin", "HR Manager")
def assign_position(position_id: int):
    validation = validate_position_assignment_payload(request.get_json(silent=True) or {})
    if not validation["is_valid"]:
        return error_response("Invalid role assignment.", status_code=422, errors=validation["errors"])

    assignment, errors = assign_position_to_employee(position_id, validation["data"]["employee_id"])
    if errors:
        return error_response("Unable to assign role.", status_code=422, errors=errors)

    return success_response(data=assignment, message="Employee role assigned")
