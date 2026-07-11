from app.api.v1.dashboard.repository import (
    count_active_employees,
    count_on_leave_today,
    count_pending_leave_requests,
    count_present_today,
    get_department_distribution,
    get_recent_announcements,
    get_recent_audit_logs,
    get_recent_employees,
    get_recent_leave_requests,
)
from app.api.v1.dashboard.schemas import serialize_dashboard, serialize_notification


def get_dashboard_stats() -> dict:
    data = {
        "stats": {
            "totalEmployees": count_active_employees(),
            "presentToday": count_present_today(),
            "onLeave": count_on_leave_today(),
            "pendingRequests": count_pending_leave_requests(),
        },
        "attendance_trend": [],
        "department_distribution": get_department_distribution(),
        "recent_employees": get_recent_employees(),
        "leave_requests": get_recent_leave_requests(),
        "recent_activity": get_recent_audit_logs(),
    }
    return serialize_dashboard(data)


def get_notifications() -> dict:
    announcements = [serialize_notification(item, "announcement") for item in get_recent_announcements()]
    audit_logs = [serialize_notification(item, "audit") for item in get_recent_audit_logs()]
    items = announcements + audit_logs
    return {
        "items": items[:10],
        "unread_count": sum(1 for item in items if item["unread"]),
    }
