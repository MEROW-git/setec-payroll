from datetime import date


def validate_review(payload):
    errors = {}
    data = {}
    for key in ("employee_id", "reviewer_id"):
        try:
            data[key] = int(payload.get(key))
            if data[key] < 1: raise ValueError
        except (TypeError, ValueError): errors[key] = ["A valid employee is required."]
    for key in ("review_date", "period_start", "period_end"):
        try: data[key] = date.fromisoformat(str(payload.get(key)))
        except (TypeError, ValueError): errors[key] = ["A valid date is required."]
    try:
        data["score"] = float(payload.get("score"))
        if not 0 <= data["score"] <= 5: raise ValueError
    except (TypeError, ValueError): errors["score"] = ["Score must be between 0 and 5."]
    data["status"] = str(payload.get("status") or "draft").lower()
    if data["status"] not in {"draft", "completed"}: errors["status"] = ["Status must be draft or completed."]
    for key in ("strengths", "improvements", "comments"):
        value = str(payload.get(key) or "").strip()
        data[key] = value or None
    if not errors and data["period_end"] < data["period_start"]: errors["period_end"] = ["Period end cannot be before period start."]
    return {"is_valid": not errors, "data": data, "errors": errors}
