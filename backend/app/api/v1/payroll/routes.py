from flask import Blueprint

from app.common.responses import success_response

payroll_bp = Blueprint("payroll", __name__)


@payroll_bp.post("/generate")
def generate_payroll():
    return success_response(message="Payroll generation endpoint ready")


@payroll_bp.get("/payslips")
def list_payslips():
    return success_response(data=[], message="Payslip endpoint ready")
