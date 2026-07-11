from app.api.v1.settings.repository import commit, email_in_use, ensure_preference, user_settings
from app.api.v1.settings.schemas import settings_data
from app.common.security import hash_password, verify_password


def get_settings(user_id):
    user = user_settings(user_id)
    return settings_data(user, ensure_preference(user)) if user else None


def update_profile(user_id, data):
    user = user_settings(user_id)
    if email_in_use(data["email"], user_id): return None, {"email": ["This email address is already in use."]}
    user.name = data["name"]; user.email = data["email"]
    if user.employee: user.employee.phone = data["phone"]
    commit(); return get_settings(user_id), None


def update_appearance(user_id, data):
    user = user_settings(user_id); preference = ensure_preference(user); preference.theme = data["theme"]; preference.density = data["density"]; commit(); return get_settings(user_id)


def update_notifications(user_id, data):
    user = user_settings(user_id); preference = ensure_preference(user)
    preference.email_notifications = data["email"]; preference.push_notifications = data["push"]; preference.leave_notifications = data["leave"]; preference.payroll_notifications = data["payroll"]
    commit(); return get_settings(user_id)


def change_password(user_id, data):
    user = user_settings(user_id)
    if not verify_password(data["current_password"], user.password_hash): return {"current_password": ["Current password is incorrect."]}
    user.password_hash = hash_password(data["new_password"]); commit(); return None
