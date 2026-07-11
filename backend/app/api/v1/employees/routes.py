from flask import Blueprint, request

from app.api.v1.employees.service import create_employee_record, delete_employee_record, get_employee_directory, get_employee_record, update_employee_record
from app.api.v1.employees.validators import validate_create_employee_payload, validate_employee_list_params, validate_employee_update_payload
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


@employees_bp.get("/<int:employee_id>")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def get_employee(employee_id: int):
    employee = get_employee_record(employee_id)
    if not employee:
        return error_response("Employee not found.", status_code=404)
    return success_response(data=employee, message="Employee loaded")


@employees_bp.patch("/<int:employee_id>")
@roles_required("Super Admin", "HR Manager")
def update_employee(employee_id: int):
    validation = validate_employee_update_payload(request.get_json(silent=True) or {})
    if not validation["is_valid"]:
        return error_response("Invalid employee data.", status_code=422, errors=validation["errors"])
    employee, errors = update_employee_record(employee_id, validation["data"])
    if errors:
        status = 404 if "employee" in errors else 409
        return error_response("Unable to update employee.", status_code=status, errors=errors)
    return success_response(data=employee, message="Employee updated")


@employees_bp.delete("/<int:employee_id>")
@roles_required("Super Admin")
def delete_employee(employee_id: int):
    if not delete_employee_record(employee_id):
        return error_response("Employee not found.", status_code=404)
    return success_response(data=None, message="Employee deleted")
