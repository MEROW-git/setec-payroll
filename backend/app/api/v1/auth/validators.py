def validate_login_payload(payload: dict) -> dict:
    errors = {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email:
        errors["email"] = ["Email is required."]
    elif "@" not in email:
        errors["email"] = ["Email must be valid."]

    if not password:
        errors["password"] = ["Password is required."]

    return {
        "is_valid": not errors,
        "errors": errors,
        "data": {
            "email": email,
            "password": password,
        },
    }
