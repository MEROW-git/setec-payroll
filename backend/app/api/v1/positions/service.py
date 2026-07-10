from app.api.v1.positions.repository import list_active_positions
from app.api.v1.positions.schemas import serialize_positions


def get_positions(department_id: str = "") -> list[dict]:
    return serialize_positions(list_active_positions(department_id=department_id))
