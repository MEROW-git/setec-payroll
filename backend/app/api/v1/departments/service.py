from app.api.v1.departments.repository import list_active_departments
from app.api.v1.departments.schemas import serialize_departments


def get_departments() -> list[dict]:
    return serialize_departments(list_active_departments())
