from app.models import Position


def serialize_position(position: Position) -> dict:
    return {
        "id": position.id,
        "department_id": position.department_id,
        "title": position.title,
        "description": position.description,
        "is_active": position.is_active,
    }


def serialize_positions(positions: list[Position]) -> list[dict]:
    return [serialize_position(position) for position in positions]


def serialize_managed_position(position: Position, employee_count: int) -> dict:
    return {
        **serialize_position(position),
        "department": position.department.name if position.department else None,
        "employee_count": employee_count,
    }
