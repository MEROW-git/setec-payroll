from app.models import Department


def serialize_department_member(employee) -> dict:
    return {
        "id": employee.id,
        "name": f"{employee.first_name} {employee.last_name}".strip(),
        "email": employee.work_email or employee.personal_email,
        "position": employee.position.title if employee.position else None,
        "status": employee.employment_status,
        "profile_photo": employee.profile_photo,
    }


def serialize_department(department: Department) -> dict:
    return {
        "id": department.id,
        "name": department.name,
        "code": department.code,
        "description": department.description,
        "annual_budget": float(department.annual_budget) if department.annual_budget is not None else None,
        "is_active": department.is_active,
    }


def serialize_departments(departments: list[Department]) -> list[dict]:
    return [serialize_department(department) for department in departments]


def serialize_managed_department(department: Department) -> dict:
    active_employees = [employee for employee in department.employees if employee.deleted_at is None]
    manager_name = None
    if department.manager:
        manager_name = f"{department.manager.first_name} {department.manager.last_name}".strip()

    return {
        **serialize_department(department),
        "manager": manager_name,
        "manager_id": department.manager_employee_id,
        "employee_count": len(active_employees),
        "member_preview": [serialize_department_member(employee) for employee in active_employees[:4]],
    }
