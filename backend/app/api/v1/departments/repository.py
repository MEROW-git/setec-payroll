from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload, selectinload

from app.extensions import db
from app.models import Department, Employee, PerformanceReview


def list_active_departments() -> list[Department]:
    return (
        Department.query.filter(
            Department.deleted_at.is_(None),
            Department.is_active.is_(True),
        )
        .order_by(Department.name.asc())
        .all()
    )


def list_managed_departments(search: str = "") -> list[Department]:
    query = Department.query.options(
        joinedload(Department.manager),
        selectinload(Department.employees).joinedload(Employee.position),
    ).filter(Department.deleted_at.is_(None), Department.is_active.is_(True))

    if search:
        pattern = f"%{search}%"
        query = query.outerjoin(Employee, Department.manager_employee_id == Employee.id).filter(
            or_(
                Department.name.ilike(pattern),
                Department.code.ilike(pattern),
                Employee.first_name.ilike(pattern),
                Employee.last_name.ilike(pattern),
            )
        )

    return query.order_by(Department.name.asc()).all()


def get_department_detail(department_id: int) -> Department | None:
    return Department.query.options(
        joinedload(Department.manager),
        selectinload(Department.employees).joinedload(Employee.position),
    ).filter(
        Department.id == department_id,
        Department.deleted_at.is_(None),
        Department.is_active.is_(True),
    ).first()


def list_department_reviews(department_id: int) -> list[PerformanceReview]:
    return PerformanceReview.query.join(Employee, PerformanceReview.employee_id == Employee.id).filter(
        Employee.department_id == department_id,
        Employee.deleted_at.is_(None),
        PerformanceReview.deleted_at.is_(None),
        PerformanceReview.score.isnot(None),
    ).order_by(PerformanceReview.review_date.asc()).all()


def get_department_by_name_or_code(name: str, code: str) -> Department | None:
    return Department.query.filter(
        Department.deleted_at.is_(None),
        or_(func.lower(Department.name) == name.lower(), func.lower(Department.code) == code.lower()),
    ).first()


def create_department(data: dict) -> Department:
    department = Department(**data)
    db.session.add(department)
    db.session.commit()
    return department
