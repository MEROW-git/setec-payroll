from flask import Blueprint

from app.api.v1.attendance.routes import attendance_bp
from app.api.v1.auth.routes import auth_bp
from app.api.v1.dashboard.routes import dashboard_bp
from app.api.v1.departments.routes import departments_bp
from app.api.v1.employees.routes import employees_bp
from app.api.v1.leave.routes import leave_bp
from app.api.v1.payroll.routes import payroll_bp
from app.api.v1.positions.routes import positions_bp
from app.api.v1.uploads.routes import uploads_bp
from app.api.v1.shifts.routes import shifts_bp
from app.api.v1.adjustments.routes import adjustments_bp
from app.api.v1.events.routes import events_bp
from app.api.v1.reports.routes import reports_bp
from app.api.v1.performance.routes import performance_bp
from app.api.v1.settings.routes import settings_bp

api_v1 = Blueprint("api_v1", __name__)

api_v1.register_blueprint(auth_bp, url_prefix="/auth")
api_v1.register_blueprint(employees_bp, url_prefix="/employees")
api_v1.register_blueprint(departments_bp, url_prefix="/departments")
api_v1.register_blueprint(positions_bp, url_prefix="/positions")
api_v1.register_blueprint(attendance_bp, url_prefix="/attendance")
api_v1.register_blueprint(leave_bp, url_prefix="/leave")
api_v1.register_blueprint(payroll_bp, url_prefix="/payroll")
api_v1.register_blueprint(dashboard_bp, url_prefix="/dashboard")
api_v1.register_blueprint(uploads_bp, url_prefix="/uploads")
api_v1.register_blueprint(shifts_bp, url_prefix="/shifts")
api_v1.register_blueprint(adjustments_bp, url_prefix="/adjustments")
api_v1.register_blueprint(events_bp, url_prefix="/events")
api_v1.register_blueprint(reports_bp, url_prefix="/reports")
api_v1.register_blueprint(performance_bp, url_prefix="/performance")
api_v1.register_blueprint(settings_bp, url_prefix="/settings")
