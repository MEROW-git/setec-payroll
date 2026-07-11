from sqlalchemy import or_
from sqlalchemy.orm import joinedload,selectinload
from app.models import Attendance,Department,Employee,EmployeeSalaryComponent,Payroll,PayrollPeriod,SalaryComponent
def period_for(start,end):return PayrollPeriod.query.filter(PayrollPeriod.start_date==start,PayrollPeriod.end_date==end).first()
def employees(search="",department_id=None):
 q=Employee.query.options(joinedload(Employee.department),selectinload(Employee.salary_components).joinedload(EmployeeSalaryComponent.salary_component)).filter(Employee.deleted_at.is_(None),Employee.employment_status=="active")
 if search:q=q.filter(or_(Employee.first_name.ilike(f"%{search}%"),Employee.last_name.ilike(f"%{search}%"),Employee.employee_code.ilike(f"%{search}%")))
 if department_id:q=q.filter(Employee.department_id==department_id)
 return q.order_by(Employee.first_name).all()
def payrolls(period_id,employee_ids):return Payroll.query.options(joinedload(Payroll.employee).joinedload(Employee.department)).filter(Payroll.payroll_period_id==period_id,Payroll.employee_id.in_(employee_ids)).all()if period_id and employee_ids else[]
def attendance(start,end,employee_ids):return Attendance.query.filter(Attendance.attendance_date.between(start,end),Attendance.employee_id.in_(employee_ids)).all()if employee_ids else[]
def components():return SalaryComponent.query.filter(SalaryComponent.deleted_at.is_(None),SalaryComponent.is_active.is_(True)).all()
