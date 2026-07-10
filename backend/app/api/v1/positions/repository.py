from app.models import Position


def list_active_positions(department_id: str = "") -> list[Position]:
    query = Position.query.filter(
        Position.deleted_at.is_(None),
        Position.is_active.is_(True),
    )

    if department_id:
        query = query.filter(Position.department_id == department_id)

    return query.order_by(Position.title.asc()).all()
