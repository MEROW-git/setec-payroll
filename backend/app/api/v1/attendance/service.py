from collections import Counter, defaultdict
from datetime import date, datetime

from app.api.v1.attendance.repository import (
    create_attendance,
    create_policy,
    get_attendance,
    get_employee,
    get_employee_by_user,
    get_policy_by_name,
    list_active_employees,
    list_attendance,
    list_employee_attendance,
    list_policies,
    save_attendance,
)
from app.api.v1.attendance.schemas import serialize_attendance, serialize_matrix_employee, serialize_policy


def get_records(start_date: date, end_date: date, search: str = "") -> dict:
    records = list_attendance(start_date, end_date, search)
    counts = Counter(record.status for record in records)
    return {
        "items": [serialize_attendance(record) for record in records],
        "stats": {status: counts.get(status, 0) for status in ("present", "late", "absent", "remote", "on_leave")},
    }


def get_my_records(user_id: int, start_date: date, end_date: date) -> tuple[dict | None, dict | None]:
    employee = get_employee_by_user(user_id)
    if not employee:
        return None, {"employee": ["No employee record is linked to this account."]}
    records = list_employee_attendance(employee.id, start_date, end_date)
    counts = Counter(record.status for record in records)
    today_record = get_attendance(employee.id, date.today())
    return {
        "employee": {"id": employee.id, "name": f"{employee.first_name} {employee.last_name}".strip(), "employee_code": employee.employee_code},
        "items": [serialize_attendance(record) for record in records],
        "stats": {status: counts.get(status, 0) for status in ("present", "late", "absent", "remote", "on_leave")},
        "today": serialize_attendance(today_record) if today_record else None,
    }, None


def remote_clock(user_id: int, action: str) -> tuple[dict | None, dict | None]:
    employee = get_employee_by_user(user_id)
    if not employee:
        return None, {"employee": ["No employee record is linked to this account."]}
    now = datetime.now()
    record = get_attendance(employee.id, now.date())
    if action == "in":
        if record:
            return None, {"clock": ["Attendance has already been started for today."]}
        record = create_attendance({
            "employee_id": employee.id,
            "attendance_date": now.date(),
            "check_in": now,
            "check_out": None,
            "work_minutes": 0,
            "overtime_minutes": 0,
            "status": "remote",
            "work_location": "Remote",
            "note": "Employee remote clock-in",
        })
    elif action == "out":
        if not record or not record.check_in:
            return None, {"clock": ["Clock in before clocking out."]}
        if record.check_out:
            return None, {"clock": ["Attendance has already been completed for today."]}
        record.check_out = now
        record.work_minutes = max(0, int((now - record.check_in).total_seconds() // 60))
        record.overtime_minutes = max(0, record.work_minutes - 480)
        save_attendance(record)
    else:
        return None, {"action": ["Action must be 'in' or 'out'."]}
    record.employee = employee
    return serialize_attendance(record), None


def get_matrix(start_date: date, end_date: date, search: str = "") -> dict:
    employees = list_active_employees(search)
    records_by_employee = defaultdict(list)
    for record in list_attendance(start_date, end_date, search):
        records_by_employee[record.employee_id].append(record)
    return {"employees": [serialize_matrix_employee(employee, records_by_employee[employee.id]) for employee in employees]}


def get_raw_punches(start_date: date, end_date: date, search: str = "") -> list[dict]:
    punches = []
    for record in list_attendance(start_date, end_date, search):
        for punch_type, timestamp in (("check_in", record.check_in), ("check_out", record.check_out)):
            if timestamp:
                punches.append({"id": f"{record.id}-{punch_type}", "employee_id": record.employee_id, "employee_name": f"{record.employee.first_name} {record.employee.last_name}".strip(), "timestamp": timestamp.isoformat(), "device": None, "method": "manual", "status": punch_type})
    return sorted(punches, key=lambda item: item["timestamp"], reverse=True)


def create_record(data: dict, approved_by: int) -> tuple[dict | None, dict | None]:
    if not get_employee(data["employee_id"]):
        return None, {"employee_id": ["Employee was not found."]}
    if get_attendance(data["employee_id"], data["attendance_date"]):
        return None, {"date": ["Attendance has already been marked for this employee and date."]}
    data["approved_by"] = approved_by
    record = create_attendance(data)
    record.employee = get_employee(record.employee_id)
    return serialize_attendance(record), None


def get_policies() -> list[dict]:
    return [serialize_policy(policy) for policy in list_policies()]


def create_policy_record(data: dict) -> tuple[dict | None, dict | None]:
    if get_policy_by_name(data["name"]):
        return None, {"name": ["A policy with this name already exists."]}
    return serialize_policy(create_policy(data)), None
