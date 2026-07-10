from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.api.v1.auth.service import authenticate_user, get_current_user_profile
from app.api.v1.auth.validators import validate_login_payload
from app.common.responses import error_response, success_response

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    validation = validate_login_payload(payload)

    if not validation["is_valid"]:
        return error_response("Invalid login request.", status_code=422, errors=validation["errors"])

    auth_payload = authenticate_user(**validation["data"])
    if not auth_payload:
        return error_response("Invalid email or password.", status_code=401)

    return success_response(data=auth_payload, message="Login successful")


@auth_bp.get("/me")
@jwt_required()
def me():
    user = get_current_user_profile(get_jwt_identity())
    if not user:
        return error_response("User not found or inactive.", status_code=401)

    return success_response(data=user, message="Authenticated user loaded")


@auth_bp.post("/register")
def register():
    return success_response(message="Register endpoint ready")


@auth_bp.post("/logout")
@jwt_required()
def logout():
    return success_response(message="Logout endpoint ready")
