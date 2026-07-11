from datetime import date

from app.api.v1.employees.repository import (
    create_employee,
    get_department_by_id,
    get_employee_by_id,
    get_employee_by_work_email,
    get_last_employee_id,
    get_position_by_id,
    list_employees,
    soft_delete_employee,
    update_employee,
)
from app.api.v1.employees.schemas import serialize_employee, serialize_employee_list
from app.common.pagination import pagination_meta


def get_employee_directory(params: dict) -> dict:
    pagination = list_employees(**params)
    meta = pagination_meta(
        page=pagination.page,
        per_page=pagination.per_page,
        total=pagination.total,
    )
    return serialize_employee_list(items=pagination.items, meta=meta)


def get_employee_record(employee_id: int) -> dict | None:
    employee = get_employee_by_id(employee_id)
    return serialize_employee(employee) if employee else None


def update_employee_record(employee_id: int, data: dict) -> tuple[dict | None, dict | None]:
    employee = get_employee_by_id(employee_id)
    if not employee:
        return None, {"employee": ["Employee was not found."]}
    if "work_email" in data:
        existing = get_employee_by_work_email(data["work_email"])
        if existing and existing.id != employee.id:
            return None, {"work_email": ["An employee with this email already exists."]}
    return serialize_employee(update_employee(employee, data)), None


def delete_employee_record(employee_id: int) -> bool:
    employee = get_employee_by_id(employee_id)
    if not employee:
        return False
    soft_delete_employee(employee)
    return True


def create_employee_record(data: dict) -> tuple[dict | None, dict | None]:
    department = get_department_by_id(data["department_id"])
    if not department:
        return None, {"department_id": ["Department was not found."]}

    position = get_position_by_id(data["position_id"])
    if not position or position.department_id != data["department_id"]:
        return None, {"position_id": ["Position was not found for the selected department."]}

    if data["manager_id"] and not get_employee_by_id(data["manager_id"]):
        return None, {"manager_id": ["Manager was not found."]}

    if get_employee_by_work_email(data["work_email"]):
        return None, {"work_email": ["An employee with this email already exists."]}

    try:
        hire_date = date.fromisoformat(data["hire_date"])
    except ValueError:
        return None, {"hire_date": ["Hire date must use YYYY-MM-DD format."]}

    next_number = get_last_employee_id() + 1
    employee_code = f"EMP{next_number:06d}"
    employee = create_employee(
        {
            "employee_code": employee_code,
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "work_email": data["work_email"],
            "phone": data["phone"],
            "department_id": data["department_id"],
            "position_id": data["position_id"],
            "manager_id": data["manager_id"],
            "hire_date": hire_date,
            "basic_salary": data["basic_salary"],
            "address": data["address"],
            "emergency_contact_name": data["emergency_contact_name"],
            "emergency_contact_phone": data["emergency_contact_phone"],
            "employment_status": data["employment_status"],
            "employment_type": data["employment_type"],
        }
    )
    return serialize_employee(employee), None
