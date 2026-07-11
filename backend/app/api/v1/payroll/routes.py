from flask import Blueprint,request
from flask_jwt_extended import get_jwt_identity
from app.api.v1.payroll.service import create_config,dashboard,eligible,get_config,get_setting,run_payroll,salary_list,settings_summary,update_setting
from app.api.v1.payroll.validators import config_payload
from app.common.decorators import roles_required
from app.common.responses import error_response,success_response
payroll_bp=Blueprint("payroll",__name__)
@payroll_bp.get("/")
@roles_required("Super Admin","HR Manager")
def overview():return success_response(dashboard((request.args.get("search")or"").strip()),"Payroll loaded")
@payroll_bp.get("/eligible")
@roles_required("Super Admin","HR Manager")
def eligible_count():return success_response({"count":eligible()},"Eligible employees loaded")
@payroll_bp.post("/run")
@roles_required("Super Admin","HR Manager")
def run():
 month=((request.get_json(silent=True)or{}).get("month")or"").strip()
 try:item,errors=run_payroll(month,int(get_jwt_identity()))
 except(ValueError,TypeError):return error_response("Month must use YYYY-MM format.",422)
 if errors:return error_response("Unable to run payroll.",409,errors)
 return success_response(item,"Payroll generated",201)
@payroll_bp.get("/salary-list")
@roles_required("Super Admin","HR Manager")
def salaries():return success_response(salary_list((request.args.get("search")or"").strip()),"Salary list loaded")
@payroll_bp.get("/settings/summary")
@roles_required("Super Admin","HR Manager")
def summary():return success_response(settings_summary(),"Payroll settings loaded")
@payroll_bp.route("/settings/<key>",methods=["GET","PUT"])
@roles_required("Super Admin","HR Manager")
def settings(key):
 if key not in{"bank","payslip"}:return error_response("Setting not found.",404)
 if request.method=="GET":return success_response(get_setting(key),"Setting loaded")
 return success_response(update_setting(key,request.get_json(silent=True)or{}),"Setting updated")
@payroll_bp.route("/config/<kind>",methods=["GET","POST"])
@roles_required("Super Admin","HR Manager")
def config(kind):
 if kind not in{"components","cycles","taxes","policies"}:return error_response("Configuration not found.",404)
 if request.method=="GET":return success_response(get_config(kind),"Payroll configuration loaded")
 validation=config_payload(kind,request.get_json(silent=True)or{})
 if not validation["is_valid"]:return error_response("Invalid configuration.",422,validation["errors"])
 item,errors=create_config(kind,validation["data"])
 if errors:return error_response("Unable to save configuration.",409,errors)
 return success_response(item,"Payroll configuration created",201)
