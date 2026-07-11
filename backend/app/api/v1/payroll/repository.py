from sqlalchemy import or_
from sqlalchemy.orm import joinedload,selectinload
from app.extensions import db
from app.models import Employee,EmployeeSalaryComponent,Payroll,PayrollCycle,PayrollPeriod,PayrollPolicy,PayrollSetting,SalaryComponent,TaxRule
def latest_period():return PayrollPeriod.query.order_by(PayrollPeriod.end_date.desc()).first()
def payroll_rows(period_id,search=""):
 q=Payroll.query.options(joinedload(Payroll.employee),joinedload(Payroll.payroll_period)).join(Employee).filter(Payroll.payroll_period_id==period_id)
 if search:q=q.filter(or_(Employee.first_name.ilike(f"%{search}%"),Employee.last_name.ilike(f"%{search}%"),Employee.employee_code.ilike(f"%{search}%")))
 return q.order_by(Employee.first_name).all()
def active_employees(search=""):
 q=Employee.query.options(joinedload(Employee.department),selectinload(Employee.salary_components).joinedload(EmployeeSalaryComponent.salary_component)).filter(Employee.deleted_at.is_(None),Employee.employment_status=="active")
 if search:q=q.filter(or_(Employee.first_name.ilike(f"%{search}%"),Employee.last_name.ilike(f"%{search}%"),Employee.employee_code.ilike(f"%{search}%")))
 return q.order_by(Employee.first_name).all()
def find_period(start,end):return PayrollPeriod.query.filter_by(start_date=start,end_date=end).first()
def active_taxes():return TaxRule.query.filter(TaxRule.deleted_at.is_(None),TaxRule.is_active.is_(True)).order_by(TaxRule.min_income).all()
def config_rows(kind):
 model={"components":SalaryComponent,"cycles":PayrollCycle,"taxes":TaxRule,"policies":PayrollPolicy}[kind];return model.query.filter(model.deleted_at.is_(None)).order_by(model.id.desc()).all()
def setting(key):return PayrollSetting.query.filter_by(setting_key=key).first()
def save_setting(key,value):
 item=setting(key)
 if item:item.setting_value=value
 else:item=PayrollSetting(setting_key=key,setting_value=value);db.session.add(item)
 db.session.commit();return item
def save(item):db.session.add(item);db.session.commit();return item
