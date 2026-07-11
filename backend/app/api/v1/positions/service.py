from app.api.v1.positions.repository import (
    create_position,
    assign_employee_position,
    get_assignable_employee_by_id,
    get_managed_position_by_id,
    get_position_by_department_and_title,
    list_active_positions,
    list_managed_positions,
)
from app.api.v1.positions.schemas import serialize_managed_position, serialize_position, serialize_positions
from app.models import Department


def get_positions(department_id: str = "") -> list[dict]:
    return serialize_positions(list_active_positions(department_id=department_id))


def get_position_management(search: str = "") -> dict:
    items = [serialize_managed_position(position, count) for position, count in list_managed_positions(search)]
    assigned = sum(1 for item in items if item["employee_count"] > 0)
    return {
        "items": items,
        "stats": {
            "total": len(items),
            "assigned": assigned,
            "unassigned": len(items) - assigned,
        },
    }


def create_position_record(data: dict) -> tuple[dict | None, dict | None]:
    department = Department.query.filter(
        Department.id == data["department_id"],
        Department.deleted_at.is_(None),
        Department.is_active.is_(True),
    ).first()
    if not department:
        return None, {"department_id": ["Department was not found."]}

    if get_position_by_department_and_title(data["department_id"], data["title"]):
        return None, {"title": ["This role already exists in the selected department."]}

    position = create_position(data)
    position.department = department
    return serialize_managed_position(position, 0), None


def assign_position_to_employee(position_id: int, employee_id: int) -> tuple[dict | None, dict | None]:
    position = get_managed_position_by_id(position_id)
    if not position:
        return None, {"position_id": ["Employee role was not found."]}

    employee = get_assignable_employee_by_id(employee_id)
    if not employee:
        return None, {"employee_id": ["Employee was not found."]}

    assign_employee_position(employee, position)
    return {
        "employee_id": employee.id,
        "position_id": position.id,
        "position": position.title,
        "department_id": position.department_id,
        "department": position.department.name if position.department else None,
    }, None
