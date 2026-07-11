from datetime import date, time


def validate_shift(payload):
    errors = {}; data = {"name": (payload.get("name") or "").strip(), "shift_type": (payload.get("shift_type") or "regular").strip(), "status": (payload.get("status") or "active").strip(), "notes": (payload.get("notes") or "").strip() or None}
    if not data["name"]: errors["name"] = ["Shift name is required."]
    for field in ("start_time", "end_time"):
        try: data[field] = time.fromisoformat(payload.get(field))
        except (TypeError, ValueError): errors[field] = [f"{field.replace('_',' ').title()} is required."]
    if data["shift_type"] not in {"regular", "weekend", "special"}: errors["shift_type"] = ["Shift type is invalid."]
    if data["status"] not in {"active", "inactive"}: errors["status"] = ["Status is invalid."]
    return {"is_valid": not errors, "errors": errors, "data": data}


def validate_request(payload):
    errors = {}; request_type = (payload.get("request_type") or "").strip()
    if request_type not in {"swap", "change"}: errors["request_type"] = ["Request type is invalid."]
    try: request_date = date.fromisoformat(payload.get("request_date"))
    except (TypeError, ValueError): request_date = None; errors["request_date"] = ["Request date is required."]
    data = {"request_type": request_type, "request_date": request_date, "remarks": (payload.get("remarks") or "").strip() or None, "status": "pending"}
    for field in ("requester_id", "current_shift_id"):
        try: data[field] = int(payload.get(field))
        except (TypeError, ValueError): errors[field] = [f"{field.replace('_',' ').title()} is required."]
    optional_field = "target_employee_id" if request_type == "swap" else "new_shift_id"
    try: data[optional_field] = int(payload.get(optional_field))
    except (TypeError, ValueError): errors[optional_field] = [f"{optional_field.replace('_',' ').title()} is required."]
    data["new_shift_id" if request_type == "swap" else "target_employee_id"] = None
    return {"is_valid": not errors, "errors": errors, "data": data}
