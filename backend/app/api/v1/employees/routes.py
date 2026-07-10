from flask import Blueprint

from app.common.responses import success_response

employees_bp = Blueprint("employees", __name__)


@employees_bp.get("/")
def list_employees():
    return success_response(data=[], message="Employee endpoints ready")
