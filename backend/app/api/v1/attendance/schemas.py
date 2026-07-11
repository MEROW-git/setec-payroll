from app.models import Attendance, AttendancePolicy, Employee


def serialize_attendance(record: Attendance) -> dict:
    employee = record.employee
    return {
        "id": record.id,
        "employee_id": record.employee_id,
        "employee_code": employee.employee_code,
        "employee_name": f"{employee.first_name} {employee.last_name}".strip(),
        "date": record.attendance_date.isoformat(),
        "check_in": record.check_in.isoformat() if record.check_in else None,
        "check_out": record.check_out.isoformat() if record.check_out else None,
        "work_minutes": record.work_minutes,
        "overtime_minutes": record.overtime_minutes,
        "location": record.work_location,
        "status": record.status,
        "note": record.note,
    }


def serialize_matrix_employee(employee: Employee, records: list[Attendance]) -> dict:
    return {
        "id": employee.id,
        "employee_code": employee.employee_code,
        "name": f"{employee.first_name} {employee.last_name}".strip(),
        "records": {record.attendance_date.isoformat(): record.status for record in records},
    }


def serialize_policy(policy: AttendancePolicy) -> dict:
    return {
        "id": policy.id,
        "name": policy.name,
        "count_type": policy.count_type,
        "considerable_value": policy.considerable_value,
        "adjusted_days": float(policy.adjusted_days),
        "description": policy.description,
        "is_active": policy.is_active,
    }
