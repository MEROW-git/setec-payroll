from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from app.api.v1.settings import validators
from app.api.v1.settings.service import change_password, get_settings, update_appearance, update_notifications, update_profile
from app.common.decorators import roles_required
from app.common.responses import error_response, success_response

settings_bp = Blueprint("settings", __name__)


@settings_bp.get("/")
@roles_required()
def read(): return success_response(get_settings(int(get_jwt_identity())), "Settings loaded")


def validated_update(validator, handler, message):
    validation = validator(request.get_json(silent=True) or {})
    if not validation["is_valid"]: return error_response("Invalid settings.", 422, validation["errors"])
    result = handler(int(get_jwt_identity()), validation["data"])
    if isinstance(result, tuple):
        data, errors = result
        if errors: return error_response("Unable to update settings.", 422, errors)
        result = data
    return success_response(result, message)


@settings_bp.put("/profile")
@roles_required()
def profile(): return validated_update(validators.profile, update_profile, "Profile updated")


@settings_bp.put("/appearance")
@roles_required()
def appearance(): return validated_update(validators.appearance, update_appearance, "Appearance updated")


@settings_bp.put("/notifications")
@roles_required()
def notifications(): return validated_update(validators.notifications, update_notifications, "Notifications updated")


@settings_bp.put("/password")
@roles_required()
def password():
    validation = validators.password(request.get_json(silent=True) or {})
    if not validation["is_valid"]: return error_response("Invalid password change.", 422, validation["errors"])
    errors = change_password(int(get_jwt_identity()), validation["data"])
    if errors: return error_response("Unable to change password.", 422, errors)
    return success_response(None, "Password changed")
