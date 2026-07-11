from calendar import monthrange
from datetime import date
from app.extensions import db
from app.models import Payroll,PayrollCycle,PayrollPeriod,PayrollPolicy,SalaryComponent,TaxRule
from app.api.v1.payroll.calculator import calculate_employee
from app.api.v1.payroll.repository import active_employees,active_taxes,config_rows,find_period,latest_period,payroll_rows,save,save_setting,setting
from app.api.v1.payroll.schemas import component_data,cycle_data,payroll_data,policy_data,tax_data
def dashboard(search=""):
 period=latest_period();rows=payroll_rows(period.id,search)if period else[];items=[payroll_data(x)for x in rows];total=sum(x["net_pay"]for x in items);processed=sum(x["status"]=="paid"for x in items)
 return{"items":items,"stats":{"total":total,"processed":processed,"employees":len(items),"pending":len(items)-processed,"next_pay_date":period.pay_date.isoformat()if period and period.pay_date else None}}
def eligible():return len(active_employees())
def run_payroll(month,user_id):
 year,number=map(int,month.split("-"));start=date(year,number,1);end=date(year,number,monthrange(year,number)[1])
 if find_period(start,end):return None,{"period":["Payroll has already been generated for this month."]}
 employees=active_employees();period=PayrollPeriod(name=start.strftime("%B %Y"),start_date=start,end_date=end,pay_date=end,status="processed",created_by=user_id);db.session.add(period);db.session.flush();rules=active_taxes()
 for employee in employees:db.session.add(Payroll(payroll_period_id=period.id,employee_id=employee.id,**calculate_employee(employee,start,end,rules)))
 db.session.commit();return{"period_id":period.id,"employees":len(employees)},None
def salary_list(search=""):
 result=[]
 for x in active_employees(search):
  last=Payroll.query.filter_by(employee_id=x.id).order_by(Payroll.id.desc()).first();result.append({"id":x.id,"name":f"{x.first_name} {x.last_name}".strip(),"employee_code":x.employee_code,"department":x.department.name if x.department else None,"base_salary":float(x.basic_salary),"net_salary":float(last.net_salary)if last else None,"last_paid":last.paid_at.date().isoformat()if last and last.paid_at else None})
 return result
def get_config(kind):
 serializer={"components":component_data,"cycles":cycle_data,"taxes":tax_data,"policies":policy_data}[kind];return[serializer(x)for x in config_rows(kind)]
def create_config(kind,data):
 model={"components":SalaryComponent,"cycles":PayrollCycle,"taxes":TaxRule,"policies":PayrollPolicy}[kind];serializer={"components":component_data,"cycles":cycle_data,"taxes":tax_data,"policies":policy_data}[kind]
 try:return serializer(save(model(**data))),None
 except Exception:db.session.rollback();return None,{"record":["A matching record exists or values are invalid."]}
def get_setting(key):
 item=setting(key);return item.setting_value if item else{}
def update_setting(key,value):return save_setting(key,value).setting_value
def settings_summary():return{"components":len([x for x in config_rows("components")if x.is_active]),"taxes":len([x for x in config_rows("taxes")if x.is_active]),"next_pay_date":dashboard()["stats"]["next_pay_date"]}
