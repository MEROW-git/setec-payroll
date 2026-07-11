from collections import defaultdict

from app.api.v1.departments.repository import (
    create_department,
    get_department_by_name_or_code,
    get_department_detail,
    list_active_departments,
    list_department_reviews,
    list_managed_departments,
)
from app.api.v1.departments.schemas import (
    serialize_department,
    serialize_department_member,
    serialize_departments,
    serialize_managed_department,
)


def get_departments() -> list[dict]:
    return serialize_departments(list_active_departments())


def get_department_management(search: str = "") -> list[dict]:
    return [serialize_managed_department(department) for department in list_managed_departments(search)]


def get_department_by_id(department_id: int) -> dict | None:
    department = get_department_detail(department_id)
    if not department:
        return None

    review_groups = defaultdict(list)
    for review in list_department_reviews(department_id):
        review_groups[review.review_date.strftime("%Y-%m")].append(float(review.score))

    performance = [
        {"month": month, "score": round(sum(scores) / len(scores), 2)}
        for month, scores in list(review_groups.items())[-6:]
    ]
    members = [
        serialize_department_member(employee)
        for employee in department.employees
        if employee.deleted_at is None
    ]
    return {
        **serialize_managed_department(department),
        "members": members,
        "performance": performance,
        "annual_budget": None,
    }


def create_department_record(data: dict) -> tuple[dict | None, dict | None]:
    if get_department_by_name_or_code(data["name"], data["code"]):
        return None, {"name": ["A department with this name or code already exists."]}
    return serialize_managed_department(create_department(data)), None
