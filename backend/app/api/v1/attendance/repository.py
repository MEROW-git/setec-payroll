from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models import Attendance, AttendancePolicy, Employee


def list_attendance(start_date: date, end_date: date, search: str = "") -> list[Attendance]:
    query = Attendance.query.options(joinedload(Attendance.employee)).join(Employee).filter(
        Attendance.attendance_date.between(start_date, end_date),
        Employee.deleted_at.is_(None),
    )
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(
            Employee.first_name.ilike(pattern),
            Employee.last_name.ilike(pattern),
            Employee.employee_code.ilike(pattern),
        ))
    return query.order_by(Attendance.attendance_date.desc(), Employee.first_name.asc()).all()


def list_employee_attendance(employee_id: int, start_date: date, end_date: date) -> list[Attendance]:
    return Attendance.query.options(joinedload(Attendance.employee)).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date.between(start_date, end_date),
    ).order_by(Attendance.attendance_date.desc()).all()


def list_active_employees(search: str = "") -> list[Employee]:
    query = Employee.query.filter(Employee.deleted_at.is_(None), Employee.employment_status == "active")
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(Employee.first_name.ilike(pattern), Employee.last_name.ilike(pattern), Employee.employee_code.ilike(pattern)))
    return query.order_by(Employee.first_name.asc(), Employee.last_name.asc()).all()


def get_employee(employee_id: int) -> Employee | None:
    return Employee.query.filter(Employee.id == employee_id, Employee.deleted_at.is_(None)).first()


def get_employee_by_user(user_id: int) -> Employee | None:
    return Employee.query.filter(Employee.user_id == user_id, Employee.deleted_at.is_(None)).first()


def get_attendance(employee_id: int, attendance_date: date) -> Attendance | None:
    return Attendance.query.filter_by(employee_id=employee_id, attendance_date=attendance_date).first()


def create_attendance(data: dict) -> Attendance:
    attendance = Attendance(**data)
    db.session.add(attendance)
    db.session.commit()
    return attendance


def save_attendance(attendance: Attendance) -> Attendance:
    db.session.add(attendance)
    db.session.commit()
    return attendance


def list_policies() -> list[AttendancePolicy]:
    return AttendancePolicy.query.filter(AttendancePolicy.deleted_at.is_(None)).order_by(AttendancePolicy.created_at.desc()).all()


def get_policy_by_name(name: str) -> AttendancePolicy | None:
    return AttendancePolicy.query.filter(AttendancePolicy.name == name, AttendancePolicy.deleted_at.is_(None)).first()


def create_policy(data: dict) -> AttendancePolicy:
    policy = AttendancePolicy(**data)
    db.session.add(policy)
    db.session.commit()
    return policy
