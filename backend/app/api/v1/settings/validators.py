import re


def profile(payload):
    errors = {}; name = str(payload.get("name") or "").strip(); email = str(payload.get("email") or "").strip().lower(); phone = str(payload.get("phone") or "").strip()
    if len(name) < 2: errors["name"] = ["Full name is required."]
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email): errors["email"] = ["A valid email is required."]
    if len(phone) > 30: errors["phone"] = ["Phone number is too long."]
    return {"is_valid": not errors, "data": {"name": name, "email": email, "phone": phone or None}, "errors": errors}


def appearance(payload):
    theme = str(payload.get("theme") or ""); density = str(payload.get("density") or ""); errors = {}
    if theme not in {"light", "dark", "system"}: errors["theme"] = ["Invalid theme."]
    if density not in {"comfortable", "compact"}: errors["density"] = ["Invalid density."]
    return {"is_valid": not errors, "data": {"theme": theme, "density": density}, "errors": errors}


def notifications(payload):
    keys = ("email", "push", "leave", "payroll"); errors = {key: ["Must be true or false."] for key in keys if not isinstance(payload.get(key), bool)}
    return {"is_valid": not errors, "data": {key: payload.get(key) for key in keys}, "errors": errors}


def password(payload):
    current = str(payload.get("current_password") or ""); new = str(payload.get("new_password") or ""); confirm = str(payload.get("confirm_password") or ""); errors = {}
    if not current: errors["current_password"] = ["Current password is required."]
    if len(new) < 8: errors["new_password"] = ["New password must contain at least 8 characters."]
    if new != confirm: errors["confirm_password"] = ["Passwords do not match."]
    return {"is_valid": not errors, "data": {"current_password": current, "new_password": new}, "errors": errors}
