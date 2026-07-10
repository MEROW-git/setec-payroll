from flask import Blueprint, request

from app.api.v1.employees.service import create_employee_record, get_employee_directory
from app.api.v1.employees.validators import validate_create_employee_payload, validate_employee_list_params
from app.common.decorators import roles_required
from app.common.responses import error_response, success_response

employees_bp = Blueprint("employees", __name__)


@employees_bp.get("/")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def list_employees():
    validation = validate_employee_list_params(request.args)
    if not validation["is_valid"]:
        return error_response("Invalid employee query parameters.", status_code=422, errors=validation["errors"])

    data = get_employee_directory(validation["data"])
    return success_response(data=data, message="Employees loaded")


@employees_bp.post("/")
@roles_required("Super Admin", "HR Manager")
def create_employee():
    validation = validate_create_employee_payload(request.get_json(silent=True) or {})
    if not validation["is_valid"]:
        return error_response("Invalid employee data.", status_code=422, errors=validation["errors"])

    employee, errors = create_employee_record(validation["data"])
    if errors:
        return error_response("Unable to create employee.", status_code=422, errors=errors)

    return success_response(data=employee, message="Employee created", status_code=201)
