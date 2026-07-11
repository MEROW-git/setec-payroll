from app.api.v1.employees.schemas import serialize_employee

COLORS = ["#0ea5e9", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#6366f1"]


def serialize_department_distribution(rows: list) -> list[dict]:
    return [
        {"name": row.name, "value": int(row.total), "color": COLORS[index % len(COLORS)]}
        for index, row in enumerate(rows)
    ]


def serialize_leave_request(request) -> dict:
    employee_name = "-"
    if request.employee:
        employee_name = f"{request.employee.first_name} {request.employee.last_name}".strip()

    return {
        "id": request.id,
        "employeeName": employee_name,
        "type": request.leave_type.name if request.leave_type else "Leave",
        "startDate": request.start_date.isoformat() if request.start_date else None,
        "endDate": request.end_date.isoformat() if request.end_date else None,
        "status": request.status.title(),
    }


def serialize_activity(log) -> dict:
    return {
        "id": log.id,
        "user": "System",
        "action": f"{log.action} {log.entity_type}",
        "time": log.created_at.isoformat() if log.created_at else None,
        "type": "audit",
    }


def serialize_notification(item, item_type: str) -> dict:
    if item_type == "announcement":
        return {
            "id": f"announcement-{item.id}",
            "title": item.title,
            "message": item.content,
            "time": (item.published_at or item.created_at).isoformat() if (item.published_at or item.created_at) else None,
            "unread": False,
            "type": "announcement",
        }

    return {
        "id": f"audit-{item.id}",
        "title": item.action.replace("_", " ").title(),
        "message": f"{item.action} on {item.entity_type}",
        "time": item.created_at.isoformat() if item.created_at else None,
        "unread": False,
        "type": "audit",
    }


def serialize_dashboard(data: dict) -> dict:
    return {
        "stats": data["stats"],
        "attendanceTrend": data["attendance_trend"],
        "departmentDistribution": serialize_department_distribution(data["department_distribution"]),
        "recentEmployees": [serialize_employee(employee) for employee in data["recent_employees"]],
        "leaveRequests": [serialize_leave_request(request) for request in data["leave_requests"]],
        "recentActivity": [serialize_activity(log) for log in data["recent_activity"]],
    }
