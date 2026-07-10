from flask import Blueprint

from app.common.responses import success_response

attendance_bp = Blueprint("attendance", __name__)


@attendance_bp.post("/check-in")
def check_in():
    return success_response(message="Check-in endpoint ready")


@attendance_bp.post("/check-out")
def check_out():
    return success_response(message="Check-out endpoint ready")


@attendance_bp.get("/history")
def history():
    return success_response(data=[], message="Attendance history endpoint ready")
