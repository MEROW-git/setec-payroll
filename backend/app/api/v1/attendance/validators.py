from datetime import date, datetime


ALLOWED_STATUSES = {"present", "late", "absent", "remote", "on_leave", "half_day", "day_off"}


def parse_iso_date(value: str, field: str, errors: dict) -> date | None:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        errors[field] = [f"{field.replace('_', ' ').title()} must be a valid date."]
        return None


def validate_record_query(args) -> dict:
    errors = {}
    start = parse_iso_date(args.get("start_date") or date.today().isoformat(), "start_date", errors)
    end = parse_iso_date(args.get("end_date") or date.today().isoformat(), "end_date", errors)
    if start and end and start > end:
        errors["date_range"] = ["Start date cannot be after end date."]
    return {"is_valid": not errors, "errors": errors, "data": {"start_date": start, "end_date": end, "search": (args.get("search") or "").strip()}}


def validate_create_attendance(payload: dict) -> dict:
    errors = {}
    attendance_date = parse_iso_date(payload.get("date"), "date", errors)
    try:
        employee_id = int(payload.get("employee_id"))
    except (TypeError, ValueError):
        employee_id = None
        errors["employee_id"] = ["Employee is required."]
    status = (payload.get("status") or "").strip()
    if status not in ALLOWED_STATUSES:
        errors["status"] = ["Attendance status is invalid."]

    def parse_time(value, field):
        if not value or not attendance_date:
            return None
        try:
            parsed = datetime.strptime(value, "%H:%M").time()
            return datetime.combine(attendance_date, parsed)
        except ValueError:
            errors[field] = [f"{field.replace('_', ' ').title()} must be a valid time."]
            return None

    check_in = parse_time(payload.get("check_in"), "check_in")
    check_out = parse_time(payload.get("check_out"), "check_out")
    if check_in and check_out and check_out < check_in:
        errors["check_out"] = ["Check out cannot be before check in."]
    work_minutes = int((check_out - check_in).total_seconds() // 60) if check_in and check_out else 0
    return {"is_valid": not errors, "errors": errors, "data": {"employee_id": employee_id, "attendance_date": attendance_date, "check_in": check_in, "check_out": check_out, "work_minutes": work_minutes, "overtime_minutes": max(0, work_minutes - 480), "status": status, "work_location": (payload.get("location") or "").strip() or None, "note": (payload.get("note") or "").strip() or None}}


def validate_policy(payload: dict) -> dict:
    errors = {}
    data = {"name": (payload.get("name") or "").strip(), "count_type": (payload.get("count_type") or "daily").strip(), "description": (payload.get("description") or "").strip() or None, "is_active": True}
    if not data["name"]:
        errors["name"] = ["Policy name is required."]
    if data["count_type"] not in {"daily", "monthly"}:
        errors["count_type"] = ["Count type is invalid."]
    try:
        data["considerable_value"] = int(payload.get("considerable_value", 0))
        data["adjusted_days"] = float(payload.get("adjusted_days", 0))
        if data["considerable_value"] < 0 or data["adjusted_days"] < 0:
            raise ValueError
    except (TypeError, ValueError):
        errors["values"] = ["Policy values must be non-negative numbers."]
    return {"is_valid": not errors, "errors": errors, "data": data}
