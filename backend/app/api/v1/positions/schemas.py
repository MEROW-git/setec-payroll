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
