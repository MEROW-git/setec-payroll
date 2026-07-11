def validate_create_position_payload(payload: dict) -> dict:
    errors = {}
    data = {
        "title": (payload.get("title") or "").strip(),
        "description": (payload.get("description") or "").strip() or None,
        "department_id": payload.get("department_id"),
        "is_active": True,
    }

    if not data["title"]:
        errors["title"] = ["Role title is required."]
    elif len(data["title"]) > 150:
        errors["title"] = ["Role title must be 150 characters or fewer."]

    if data["description"] and len(data["description"]) > 2000:
        errors["description"] = ["Description must be 2000 characters or fewer."]

    try:
        data["department_id"] = int(data["department_id"])
    except (TypeError, ValueError):
        errors["department_id"] = ["Department is required."]

    return {"is_valid": not errors, "errors": errors, "data": data}


def validate_position_assignment_payload(payload: dict) -> dict:
    try:
        employee_id = int(payload.get("employee_id"))
        if employee_id < 1:
            raise ValueError
    except (TypeError, ValueError):
        return {
            "is_valid": False,
            "errors": {"employee_id": ["A valid employee is required."]},
            "data": {},
        }

    return {"is_valid": True, "errors": {}, "data": {"employee_id": employee_id}}
