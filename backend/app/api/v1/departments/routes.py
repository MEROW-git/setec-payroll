from flask import Blueprint, request

from app.api.v1.departments.service import (
    create_department_record,
    get_department_by_id,
    get_department_management,
    get_departments,
)
from app.api.v1.departments.validators import validate_create_department_payload
from app.common.decorators import roles_required
from app.common.responses import error_response, success_response

departments_bp = Blueprint("departments", __name__)


@departments_bp.get("/management")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def department_management():
    data = get_department_management(search=(request.args.get("search") or "").strip())
    return success_response(data=data, message="Department management loaded")


@departments_bp.get("/")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def list_departments():
    return success_response(data=get_departments(), message="Departments loaded")


@departments_bp.get("/<int:department_id>")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def department_detail(department_id: int):
    data = get_department_by_id(department_id)
    if not data:
        return error_response("Department not found.", status_code=404)
    return success_response(data=data, message="Department details loaded")


@departments_bp.post("/")
@roles_required("Super Admin", "HR Manager")
def add_department():
    validation = validate_create_department_payload(request.get_json(silent=True) or {})
    if not validation["is_valid"]:
        return error_response("Invalid department data.", status_code=422, errors=validation["errors"])

    department, errors = create_department_record(validation["data"])
    if errors:
        return error_response("Unable to create department.", status_code=409, errors=errors)
    return success_response(data=department, message="Department created", status_code=201)
