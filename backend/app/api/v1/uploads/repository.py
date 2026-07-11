from app.extensions import db
from app.models import Employee


def get_employee(employee_id: int) -> Employee | None:
    return Employee.query.filter(Employee.id == employee_id, Employee.deleted_at.is_(None)).first()


def save_profile_photo(employee: Employee, secure_url: str) -> None:
    employee.profile_photo = secure_url
    db.session.commit()
