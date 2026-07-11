from datetime import date
from flask import Blueprint,request
from app.api.v1.reports.service import report
from app.common.decorators import roles_required
from app.common.responses import error_response,success_response
reports_bp=Blueprint("reports",__name__)
@reports_bp.get("/<kind>")
@roles_required("Super Admin","HR Manager","Department Manager")
def generate(kind):
 if kind not in{"monthly-salary","salary-summary","bank-advice","payslip","attendance","yearly-ctc","components"}:return error_response("Report not found.",404)
 month=(request.args.get("month")or date.today().strftime("%Y-%m")).strip();department=request.args.get("department_id")
 try:data=report(kind,month,(request.args.get("search")or"").strip(),int(department)if department else None)
 except(ValueError,TypeError):return error_response("Invalid report filters.",422)
 return success_response(data,"Report generated")
