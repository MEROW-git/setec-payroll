from calendar import monthrange
from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from app.api.v1.attendance.service import create_policy_record, create_record, get_matrix, get_my_records, get_policies, get_raw_punches, get_records, remote_clock
from app.api.v1.attendance.validators import validate_create_attendance, validate_policy, validate_record_query
from app.common.decorators import roles_required
from app.common.responses import error_response, success_response

attendance_bp = Blueprint("attendance", __name__)


@attendance_bp.get("/me")
@roles_required("Employee")
def my_records():
    validation = validate_record_query(request.args)
    if not validation["is_valid"]:
        return error_response("Invalid attendance query.", 422, validation["errors"])
    data, errors = get_my_records(int(get_jwt_identity()), validation["data"]["start_date"], validation["data"]["end_date"])
    if errors:
        return error_response("Unable to load your attendance.", 409, errors)
    return success_response(data, "Your attendance records loaded")


@attendance_bp.post("/me/clock")
@roles_required("Employee")
def clock_remote():
    action = str((request.get_json(silent=True) or {}).get("action") or "").strip().lower()
    record, errors = remote_clock(int(get_jwt_identity()), action)
    if errors:
        return error_response("Unable to update remote attendance.", 409, errors)
    return success_response(record, f"Remote clock {action} recorded")


@attendance_bp.get("/records")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def records():
    validation = validate_record_query(request.args)
    if not validation["is_valid"]:
        return error_response("Invalid attendance query.", 422, validation["errors"])
    data = validation["data"]
    return success_response(get_records(**data), "Attendance records loaded")


@attendance_bp.get("/matrix")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def matrix():
    month = (request.args.get("month") or date.today().strftime("%Y-%m")).strip()
    try:
        year, month_number = map(int, month.split("-"))
        start_date = date(year, month_number, 1)
        end_date = date(year, month_number, monthrange(year, month_number)[1])
    except (TypeError, ValueError):
        return error_response("Month must use YYYY-MM format.", 422)
    return success_response(get_matrix(start_date, end_date, (request.args.get("search") or "").strip()), "Attendance matrix loaded")


@attendance_bp.get("/raw-punches")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def raw_punches():
    validation = validate_record_query(request.args)
    if not validation["is_valid"]:
        return error_response("Invalid punch query.", 422, validation["errors"])
    return success_response(get_raw_punches(**validation["data"]), "Raw punches loaded")


@attendance_bp.post("/records")
@roles_required("Super Admin", "HR Manager")
def mark_attendance():
    validation = validate_create_attendance(request.get_json(silent=True) or {})
    if not validation["is_valid"]:
        return error_response("Invalid attendance data.", 422, validation["errors"])
    record, errors = create_record(validation["data"], int(get_jwt_identity()))
    if errors:
        return error_response("Unable to mark attendance.", 409, errors)
    return success_response(record, "Attendance marked", 201)


@attendance_bp.get("/devices")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def devices():
    return success_response([], "No attendance devices registered")


@attendance_bp.get("/policies")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def policies():
    return success_response(get_policies(), "Attendance policies loaded")


@attendance_bp.post("/policies")
@roles_required("Super Admin", "HR Manager")
def add_policy():
    validation = validate_policy(request.get_json(silent=True) or {})
    if not validation["is_valid"]:
        return error_response("Invalid attendance policy.", 422, validation["errors"])
    policy, errors = create_policy_record(validation["data"])
    if errors:
        return error_response("Unable to create policy.", 409, errors)
    return success_response(policy, "Attendance policy created", 201)
