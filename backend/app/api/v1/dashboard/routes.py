from flask import Blueprint

from app.api.v1.dashboard.service import get_dashboard_stats, get_notifications
from app.common.decorators import roles_required
from app.common.responses import success_response

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/stats")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def stats():
    return success_response(data=get_dashboard_stats(), message="Dashboard statistics loaded")


@dashboard_bp.get("/notifications")
@roles_required("Super Admin", "HR Manager", "Department Manager", "Employee")
def notifications():
    return success_response(data=get_notifications(), message="Notifications loaded")
