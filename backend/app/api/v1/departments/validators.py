import re


def validate_create_department_payload(payload: dict) -> dict:
    errors = {}
    data = {
        "name": (payload.get("name") or "").strip(),
        "code": (payload.get("code") or "").strip().upper(),
        "description": (payload.get("description") or "").strip() or None,
        "manager_employee_id": payload.get("manager_employee_id") or None,
        "annual_budget": payload.get("annual_budget") or None,
        "is_active": True,
    }

    if not data["name"]:
        errors["name"] = ["Department name is required."]
    elif len(data["name"]) > 150:
        errors["name"] = ["Department name must be 150 characters or fewer."]

    if not data["code"]:
        errors["code"] = ["Department code is required."]
    elif len(data["code"]) > 30 or not re.fullmatch(r"[A-Z0-9_-]+", data["code"]):
        errors["code"] = ["Code may contain only letters, numbers, hyphens, and underscores."]

    try:
        data["manager_employee_id"] = int(data["manager_employee_id"]) if data["manager_employee_id"] else None
    except (TypeError, ValueError):
        errors["manager_employee_id"] = ["Manager must be a valid employee."]

    try:
        data["annual_budget"] = float(data["annual_budget"]) if data["annual_budget"] is not None else None
        if data["annual_budget"] is not None and data["annual_budget"] < 0:
            errors["annual_budget"] = ["Annual budget cannot be negative."]
    except (TypeError, ValueError):
        errors["annual_budget"] = ["Annual budget must be numeric."]

    return {"is_valid": not errors, "errors": errors, "data": data}
