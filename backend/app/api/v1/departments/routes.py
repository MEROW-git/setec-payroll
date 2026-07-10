from flask import Blueprint

from app.common.responses import success_response

departments_bp = Blueprint("departments", __name__)


@departments_bp.get("/")
def list_departments():
    return success_response(data=[], message="Department endpoints ready")
