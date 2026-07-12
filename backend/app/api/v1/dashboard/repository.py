from collections import Counter, defaultdict
from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.models import Announcement, Attendance, AuditLog, Department, Employee, LeaveRequest


def count_active_employees() -> int:
    return Employee.query.filter(Employee.deleted_at.is_(None), Employee.employment_status == "active").count()


def count_present_today() -> int:
    return Attendance.query.filter(
        Attendance.attendance_date == date.today(),
        Attendance.status == "present",
    ).count()


def count_on_leave_today() -> int:
    today = date.today()
    return LeaveRequest.query.filter(
        LeaveRequest.deleted_at.is_(None),
        LeaveRequest.status == "approved",
        LeaveRequest.start_date <= today,
        LeaveRequest.end_date >= today,
    ).count()


def count_pending_leave_requests() -> int:
    return LeaveRequest.query.filter(
        LeaveRequest.deleted_at.is_(None),
        LeaveRequest.status == "pending",
    ).count()


def get_attendance_trend() -> list[dict]:
    today = date.today()
    start = date(today.year, 1, 1)
    records = Attendance.query.filter(
        Attendance.attendance_date.between(start, today),
    ).with_entities(Attendance.attendance_date, Attendance.status).all()

    monthly = defaultdict(Counter)
    for attendance_date, status in records:
        monthly[attendance_date.month][status] += 1

    return [
        {
            "name": date(today.year, month, 1).strftime("%b"),
            "present": monthly[month]["present"],
            "absent": monthly[month]["absent"],
            "onLeave": monthly[month]["on_leave"],
        }
        for month in range(1, today.month + 1)
    ]


def get_department_distribution() -> list:
    return (
        Department.query.outerjoin(Employee, Department.id == Employee.department_id)
        .filter(Department.deleted_at.is_(None))
        .with_entities(Department.name, func.count(Employee.id).label("total"))
        .group_by(Department.id, Department.name)
        .order_by(Department.name.asc())
        .all()
    )


def get_recent_employees(limit: int = 5) -> list[Employee]:
    return (
        Employee.query.options(joinedload(Employee.department), joinedload(Employee.position))
        .filter(Employee.deleted_at.is_(None))
        .order_by(Employee.created_at.desc())
        .limit(limit)
        .all()
    )


def get_recent_leave_requests(limit: int = 3) -> list[LeaveRequest]:
    return (
        LeaveRequest.query.options(joinedload(LeaveRequest.employee), joinedload(LeaveRequest.leave_type))
        .filter(LeaveRequest.deleted_at.is_(None))
        .order_by(LeaveRequest.created_at.desc())
        .limit(limit)
        .all()
    )


def get_recent_audit_logs(limit: int = 5) -> list[AuditLog]:
    return (
        AuditLog.query.with_entities(
            AuditLog.id,
            AuditLog.action,
            AuditLog.entity_type,
            AuditLog.entity_id,
            AuditLog.created_at,
        )
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .all()
    )


def get_recent_announcements(limit: int = 5) -> list[Announcement]:
    return (
        Announcement.query.filter(
            Announcement.deleted_at.is_(None),
            Announcement.status == "published",
        )
        .order_by(Announcement.published_at.desc(), Announcement.created_at.desc())
        .limit(limit)
        .all()
    )
