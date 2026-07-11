from app.models import Employee


def serialize_employee(employee: Employee) -> dict:
    full_name = f"{employee.first_name} {employee.last_name}".strip()
    return {
        "id": employee.id,
        "employee_code": employee.employee_code,
        "name": full_name,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.work_email or employee.personal_email,
        "department": employee.department.name if employee.department else None,
        "department_id": employee.department_id,
        "position": employee.position.title if employee.position else None,
        "position_id": employee.position_id,
        "status": employee.employment_status,
        "employment_type": employee.employment_type,
        "profile_photo": employee.profile_photo,
        "hire_date": employee.hire_date.isoformat() if employee.hire_date else None,
        "phone": employee.phone,
        "address": employee.address,
        "basic_salary": float(employee.basic_salary or 0),
        "manager": employee.manager.first_name + " " + employee.manager.last_name if employee.manager else None,
        "emergency_contact_name": employee.emergency_contact_name,
        "emergency_contact_phone": employee.emergency_contact_phone,
    }


def serialize_employee_list(items: list[Employee], meta: dict) -> dict:
    return {
        "items": [serialize_employee(employee) for employee in items],
        "meta": meta,
    }
