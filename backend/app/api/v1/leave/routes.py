from flask import Blueprint

from app.common.responses import success_response

leave_bp = Blueprint("leave", __name__)


@leave_bp.post("/")
def apply_leave():
    return success_response(message="Leave application endpoint ready")


@leave_bp.post("/<int:leave_id>/approve")
def approve_leave(leave_id: int):
    return success_response(data={"leave_id": leave_id}, message="Leave approval endpoint ready")


@leave_bp.post("/<int:leave_id>/reject")
def reject_leave(leave_id: int):
    return success_response(data={"leave_id": leave_id}, message="Leave rejection endpoint ready")
