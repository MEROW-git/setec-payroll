from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models import Department, Employee, Position


def list_employees(page: int, per_page: int, search: str = "", status: str = "", department_id: str = ""):
    query = (
        Employee.query.options(
            joinedload(Employee.department),
            joinedload(Employee.position),
        )
        .filter(Employee.deleted_at.is_(None))
        .join(Department, Employee.department_id == Department.id)
        .join(Position, Employee.position_id == Position.id)
    )

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Employee.employee_code.ilike(pattern),
                Employee.first_name.ilike(pattern),
                Employee.last_name.ilike(pattern),
                Employee.work_email.ilike(pattern),
                Employee.personal_email.ilike(pattern),
                Department.name.ilike(pattern),
                Position.title.ilike(pattern),
            )
        )

    if status:
        query = query.filter(Employee.employment_status == status)

    if department_id:
        query = query.filter(Employee.department_id == department_id)

    return query.order_by(Employee.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )


def get_department_by_id(department_id: int) -> Department | None:
    return Department.query.filter(
        Department.id == department_id,
        Department.deleted_at.is_(None),
        Department.is_active.is_(True),
    ).first()


def get_position_by_id(position_id: int) -> Position | None:
    return Position.query.filter(
        Position.id == position_id,
        Position.deleted_at.is_(None),
        Position.is_active.is_(True),
    ).first()


def get_employee_by_id(employee_id: int) -> Employee | None:
    return Employee.query.filter(Employee.id == employee_id, Employee.deleted_at.is_(None)).first()


def get_employee_by_work_email(email: str) -> Employee | None:
    return Employee.query.filter(Employee.work_email == email, Employee.deleted_at.is_(None)).first()


def get_last_employee_id() -> int:
    employee = Employee.query.order_by(Employee.id.desc()).first()
    return int(employee.id) if employee else 0


def create_employee(data: dict) -> Employee:
    employee = Employee(**data)
    db.session.add(employee)
    db.session.commit()
    return employee
