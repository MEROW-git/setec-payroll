from flask import Blueprint

from app.common.responses import success_response

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/stats")
def stats():
    return success_response(data={}, message="Dashboard statistics endpoint ready")
