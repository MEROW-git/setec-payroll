from app.models import Department


def serialize_department(department: Department) -> dict:
    return {
        "id": department.id,
        "name": department.name,
        "code": department.code,
        "description": department.description,
        "is_active": department.is_active,
    }


def serialize_departments(departments: list[Department]) -> list[dict]:
    return [serialize_department(department) for department in departments]
