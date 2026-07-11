def validate_employee_list_params(args) -> dict:
    errors = {}

    try:
        page = int(args.get("page", 1))
    except ValueError:
        page = 1
        errors["page"] = ["Page must be a number."]

    try:
        per_page = int(args.get("per_page", 12))
    except ValueError:
        per_page = 12
        errors["per_page"] = ["Per page must be a number."]

    if page < 1:
        errors["page"] = ["Page must be at least 1."]

    if per_page < 1 or per_page > 100:
        errors["per_page"] = ["Per page must be between 1 and 100."]

    return {
        "is_valid": not errors,
        "errors": errors,
        "data": {
            "page": page,
            "per_page": per_page,
            "search": (args.get("search") or "").strip(),
            "status": (args.get("status") or "").strip(),
            "department_id": (args.get("department_id") or "").strip(),
        },
    }


def validate_create_employee_payload(payload: dict) -> dict:
    errors = {}

    data = {
        "first_name": (payload.get("first_name") or "").strip(),
        "last_name": (payload.get("last_name") or "").strip(),
        "work_email": (payload.get("work_email") or "").strip().lower(),
        "phone": (payload.get("phone") or "").strip() or None,
        "department_id": payload.get("department_id"),
        "position_id": payload.get("position_id"),
        "manager_id": payload.get("manager_id") or None,
        "hire_date": (payload.get("hire_date") or "").strip(),
        "basic_salary": payload.get("basic_salary") or 0,
        "address": (payload.get("address") or "").strip() or None,
        "emergency_contact_name": (payload.get("emergency_contact_name") or "").strip() or None,
        "emergency_contact_phone": (payload.get("emergency_contact_phone") or "").strip() or None,
        "employment_status": (payload.get("employment_status") or "active").strip(),
        "employment_type": (payload.get("employment_type") or "full_time").strip(),
    }

    for field in ("first_name", "last_name", "work_email", "department_id", "position_id", "hire_date"):
        if not data[field]:
            errors[field] = [f"{field.replace('_', ' ').title()} is required."]

    if data["work_email"] and "@" not in data["work_email"]:
        errors["work_email"] = ["Email must be valid."]

    try:
        data["department_id"] = int(data["department_id"]) if data["department_id"] else None
    except (TypeError, ValueError):
        errors["department_id"] = ["Department must be valid."]

    try:
        data["position_id"] = int(data["position_id"]) if data["position_id"] else None
    except (TypeError, ValueError):
        errors["position_id"] = ["Position must be valid."]

    try:
        data["manager_id"] = int(data["manager_id"]) if data["manager_id"] else None
    except (TypeError, ValueError):
        errors["manager_id"] = ["Manager must be valid."]

    try:
        data["basic_salary"] = float(data["basic_salary"])
        if data["basic_salary"] < 0:
            errors["basic_salary"] = ["Basic salary cannot be negative."]
    except (TypeError, ValueError):
        errors["basic_salary"] = ["Basic salary must be numeric."]

    return {
        "is_valid": not errors,
        "errors": errors,
        "data": data,
    }


def validate_employee_update_payload(payload: dict) -> dict:
    allowed = {"first_name", "last_name", "phone", "work_email", "employment_status"}
    data = {key: value.strip() if isinstance(value, str) else value for key, value in payload.items() if key in allowed}
    errors = {}
    if not data:
        errors["payload"] = ["At least one employee field is required."]
    if "first_name" in data and not data["first_name"]:
        errors["first_name"] = ["First name is required."]
    if "last_name" in data and not data["last_name"]:
        errors["last_name"] = ["Last name is required."]
    if "work_email" in data:
        data["work_email"] = data["work_email"].lower()
        if "@" not in data["work_email"]:
            errors["work_email"] = ["Email must be valid."]
    if "employment_status" in data and data["employment_status"] not in {"active", "inactive", "on_leave", "terminated"}:
        errors["employment_status"] = ["Status is not supported."]
    return {"is_valid": not errors, "errors": errors, "data": data}
