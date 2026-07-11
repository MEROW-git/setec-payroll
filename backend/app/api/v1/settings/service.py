from app.api.v1.settings.repository import commit, email_in_use, ensure_preference, user_settings
from app.api.v1.settings.schemas import settings_data
from app.common.security import hash_password, verify_password
from datetime import date
from sqlalchemy import func
from app.models import Attendance, EmployeeShiftAssignment, LeaveRequest, LeaveType, Payroll, PerformanceReview


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


def profile_overview(user_id):
    user = user_settings(user_id)
    employee = user.employee
    base = {
        "account": {"id": user.id, "name": user.name, "email": user.email, "role": user.role.name if user.role else None, "is_active": user.is_active, "created_at": user.created_at.isoformat(), "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None},
        "employee": None,
        "stats": {"leave_balance": None, "attendance": None, "salary": None, "performance": None},
    }
    if not employee: return base
    today = date.today(); month_start = today.replace(day=1)
    attendance_total = Attendance.query.filter(Attendance.employee_id == employee.id, Attendance.attendance_date.between(month_start, today)).count()
    attendance_present = Attendance.query.filter(Attendance.employee_id == employee.id, Attendance.attendance_date.between(month_start, today), Attendance.status.in_(("present", "late", "half_day"))).count()
    annual = LeaveType.query.filter(LeaveType.code == "ANNUAL", LeaveType.deleted_at.is_(None)).first()
    used = 0.0
    if annual:
        used = float(LeaveRequest.query.with_entities(func.coalesce(func.sum(LeaveRequest.total_days), 0)).filter(LeaveRequest.employee_id == employee.id, LeaveRequest.leave_type_id == annual.id, LeaveRequest.status == "approved", LeaveRequest.start_date >= date(today.year, 1, 1), LeaveRequest.deleted_at.is_(None)).scalar() or 0)
    latest_payroll = Payroll.query.filter(Payroll.employee_id == employee.id).order_by(Payroll.created_at.desc()).first()
    latest_review = PerformanceReview.query.filter(PerformanceReview.employee_id == employee.id, PerformanceReview.status == "completed", PerformanceReview.deleted_at.is_(None)).order_by(PerformanceReview.review_date.desc()).first()
    assignment = EmployeeShiftAssignment.query.filter(EmployeeShiftAssignment.employee_id == employee.id, EmployeeShiftAssignment.is_active.is_(True)).order_by(EmployeeShiftAssignment.effective_from.desc()).first()
    base["employee"] = {
        "id": employee.id, "employee_code": employee.employee_code, "name": f"{employee.first_name} {employee.last_name}".strip(), "email": employee.work_email or employee.personal_email, "phone": employee.phone, "personal_email": employee.personal_email, "address": employee.address, "department": employee.department.name if employee.department else None, "position": employee.position.title if employee.position else None, "manager": f"{employee.manager.first_name} {employee.manager.last_name}".strip() if employee.manager else None, "status": employee.employment_status, "employment_type": employee.employment_type, "hire_date": employee.hire_date.isoformat() if employee.hire_date else None, "probation_end_date": employee.probation_end_date.isoformat() if employee.probation_end_date else None, "basic_salary": float(employee.basic_salary), "bank_name": employee.bank_name, "bank_account_name": employee.bank_account_name, "bank_account_number": employee.bank_account_number, "emergency_contact_name": employee.emergency_contact_name, "emergency_contact_phone": employee.emergency_contact_phone, "shift": assignment.shift.name if assignment else None,
    }
    base["stats"] = {"leave_balance": max(float(annual.days_per_year) - used, 0) if annual else None, "attendance": round(attendance_present / attendance_total * 100, 1) if attendance_total else None, "salary": float(latest_payroll.net_salary) if latest_payroll else float(employee.basic_salary), "performance": float(latest_review.score) if latest_review and latest_review.score is not None else None}
    return base
