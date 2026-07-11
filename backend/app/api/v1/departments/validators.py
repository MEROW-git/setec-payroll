import re


def validate_create_department_payload(payload: dict) -> dict:
    errors = {}
    data = {
        "name": (payload.get("name") or "").strip(),
        "code": (payload.get("code") or "").strip().upper(),
        "description": (payload.get("description") or "").strip() or None,
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

    return {"is_valid": not errors, "errors": errors, "data": data}
