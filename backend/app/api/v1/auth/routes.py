from flask import Blueprint

from app.common.responses import success_response

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    return success_response(message="Login endpoint ready")


@auth_bp.post("/register")
def register():
    return success_response(message="Register endpoint ready")


@auth_bp.post("/logout")
def logout():
    return success_response(message="Logout endpoint ready")
