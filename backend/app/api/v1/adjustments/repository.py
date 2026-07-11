from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.models import Employee,EmployeeSalaryComponent,SalaryComponent

def list_entries(start,end,search="",component_type="",status=""):
    query=EmployeeSalaryComponent.query.options(joinedload(EmployeeSalaryComponent.employee),joinedload(EmployeeSalaryComponent.salary_component)).join(Employee).join(SalaryComponent).filter(EmployeeSalaryComponent.deleted_at.is_(None),EmployeeSalaryComponent.effective_date.between(start,end))
    if search:
        pattern=f"%{search}%";query=query.filter(or_(Employee.first_name.ilike(pattern),Employee.last_name.ilike(pattern),Employee.employee_code.ilike(pattern)))
    if component_type:query=query.filter(SalaryComponent.component_type==component_type)
    if status:query=query.filter(EmployeeSalaryComponent.status==status)
    return query.order_by(EmployeeSalaryComponent.effective_date.desc()).all()
def get_employee(item_id):return Employee.query.filter(Employee.id==item_id,Employee.deleted_at.is_(None)).first()
def find_component(name,kind):return SalaryComponent.query.filter(SalaryComponent.name==name,SalaryComponent.component_type==kind,SalaryComponent.deleted_at.is_(None)).first()
def save_entry(data,category,kind):
    component=find_component(category,kind)
    if not component:
        base="".join(character if character.isalnum() else "_" for character in category.upper()).strip("_")[:35]or"MANUAL";code=f"{kind[:3].upper()}_{base}"
        suffix=1
        while SalaryComponent.query.filter_by(code=code).first():suffix+=1;code=f"{kind[:3].upper()}_{base}_{suffix}"
        component=SalaryComponent(name=category,code=code,component_type=kind,calculation_type="fixed",default_amount=0,is_taxable=False,is_active=True);db.session.add(component);db.session.flush()
    entry=EmployeeSalaryComponent(salary_component_id=component.id,**data);db.session.add(entry);db.session.commit();entry.salary_component=component;entry.employee=get_employee(entry.employee_id);return entry
