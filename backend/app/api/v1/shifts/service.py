from app.api.v1.shifts.repository import (
    active_assignment, create_request, create_shift, finalize_request, get_employee, get_request,
    get_shift, get_shift_by_name, list_requests, list_shifts,
)
from app.api.v1.shifts.schemas import serialize_request, serialize_shift


def get_shift_management(search=""):
    rows = list_shifts(search); items = [serialize_shift(shift, count) for shift, count in rows]
    return {"items": items, "stats": {"active": sum(item["status"] == "active" for item in items), "inactive": sum(item["status"] == "inactive" for item in items), "employees": sum(item["employee_count"] for item in items)}}


def create_shift_record(data):
    if get_shift_by_name(data["name"]): return None, {"name": ["A shift with this name already exists."]}
    return serialize_shift(create_shift(data)), None


def get_shift_requests(search=""):
    items = [serialize_request(item) for item in list_requests(search)]
    return {"items": items, "pending_count": sum(item["status"] == "pending" for item in items)}


def create_shift_request(data):
    if not get_employee(data["requester_id"]): return None, {"requester_id": ["Requesting employee was not found."]}
    if not get_shift(data["current_shift_id"]): return None, {"current_shift_id": ["Current shift was not found."]}
    if data["request_type"] == "swap":
        if data["target_employee_id"] == data["requester_id"]: return None, {"target_employee_id": ["Employees must be different."]}
        if not get_employee(data["target_employee_id"]): return None, {"target_employee_id": ["Target employee was not found."]}
    elif not get_shift(data["new_shift_id"]): return None, {"new_shift_id": ["New shift was not found."]}
    return serialize_request(create_request(data)), None


def review_request(request_id, status, reviewer_id):
    item = get_request(request_id)
    if not item: return None, {"request": ["Shift request was not found."]}
    if item.status != "pending": return None, {"status": ["This request has already been reviewed."]}
    if status not in {"approved", "rejected"}: return None, {"status": ["Review status is invalid."]}
    if status == "approved" and item.request_type == "swap" and not active_assignment(item.target_employee_id):
        return None, {"target_employee_id": ["Target employee has no active shift to swap."]}
    finalize_request(item, status, reviewer_id)
    return serialize_request(get_request(item.id)), None
