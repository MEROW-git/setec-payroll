from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models import Department, Employee, Position


def list_active_positions(department_id: str = "") -> list[Position]:
    query = Position.query.filter(
        Position.deleted_at.is_(None),
        Position.is_active.is_(True),
    )

    if department_id:
        query = query.filter(Position.department_id == department_id)

    return query.order_by(Position.title.asc()).all()


def list_managed_positions(search: str = "") -> list[tuple[Position, int]]:
    query = (
        db.session.query(Position, func.count(Employee.id).label("employee_count"))
        .options(joinedload(Position.department))
        .outerjoin(Employee, (Employee.position_id == Position.id) & Employee.deleted_at.is_(None))
        .join(Department, Position.department_id == Department.id)
        .filter(Position.deleted_at.is_(None), Position.is_active.is_(True))
        .group_by(Position.id)
    )

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Position.title.ilike(pattern),
                Position.description.ilike(pattern),
                Department.name.ilike(pattern),
            )
        )

    return query.order_by(Position.title.asc()).all()


def get_position_by_department_and_title(department_id: int, title: str) -> Position | None:
    return Position.query.filter(
        Position.department_id == department_id,
        func.lower(Position.title) == title.lower(),
        Position.deleted_at.is_(None),
    ).first()


def create_position(data: dict) -> Position:
    position = Position(**data)
    db.session.add(position)
    db.session.commit()
    return position


def get_managed_position_by_id(position_id: int) -> Position | None:
    return Position.query.options(joinedload(Position.department)).filter(
        Position.id == position_id,
        Position.deleted_at.is_(None),
        Position.is_active.is_(True),
    ).first()


def get_assignable_employee_by_id(employee_id: int) -> Employee | None:
    return Employee.query.filter(
        Employee.id == employee_id,
        Employee.deleted_at.is_(None),
    ).first()


def assign_employee_position(employee: Employee, position: Position) -> Employee:
    employee.position_id = position.id
    employee.department_id = position.department_id
    db.session.commit()
    return employee
