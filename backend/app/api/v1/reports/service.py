from calendar import monthrange
from collections import Counter,defaultdict
from datetime import date
from app.api.v1.reports.repository import attendance,components,employees,payrolls,period_for
def month_dates(month):year,number=map(int,month.split("-"));return date(year,number,1),date(year,number,monthrange(year,number)[1])
def payroll_row(item):return{"employee_id":item.employee_id,"employee_name":f"{item.employee.first_name} {item.employee.last_name}".strip(),"employee_code":item.employee.employee_code,"department":item.employee.department.name if item.employee.department else None,"basic":float(item.basic_salary),"allowances":float(item.total_allowance+item.bonus),"deductions":float(item.total_deduction+item.tax_amount),"net":float(item.net_salary),"status":item.payment_status,"bank_name":item.employee.bank_name,"bank_account":item.employee.bank_account_number}
def report(kind,month,search="",department_id=None):
 start,end=month_dates(month);staff=employees(search,department_id);ids=[x.id for x in staff];period=period_for(start,end);rows=[payroll_row(x)for x in payrolls(period.id if period else None,ids)]
 if kind=="monthly-salary":return{"rows":rows}
 if kind=="salary-summary":
  departments=defaultdict(float)
  for row in rows:departments[row["department"]or"Unassigned"]+=row["net"]
  return{"totals":{"gross":sum(x["basic"]+x["allowances"]for x in rows),"allowances":sum(x["allowances"]for x in rows),"deductions":sum(x["deductions"]for x in rows)},"departments":[{"name":name,"amount":amount}for name,amount in departments.items()]}
 if kind=="bank-advice":return{"rows":[{"employee_name":x["employee_name"],"account_number":x["bank_account"],"bank_name":x["bank_name"],"amount":x["net"]}for x in rows]}
 if kind=="payslip":return{"rows":rows}
 if kind=="attendance":
  grouped=defaultdict(Counter)
  for item in attendance(start,end,ids):grouped[item.employee_id][item.status]+=1
  working=sum(1 for day in range(1,end.day+1)if date(start.year,start.month,day).weekday()<5)
  return{"rows":[{"employee_id":x.id,"employee_name":f"{x.first_name} {x.last_name}".strip(),"employee_code":x.employee_code,"working_days":working,"present":grouped[x.id]["present"],"absent":grouped[x.id]["absent"],"late":grouped[x.id]["late"],"leave":grouped[x.id]["on_leave"]}for x in staff]}
 if kind=="yearly-ctc":
  result=[]
  for employee in staff:
   allowance=bonus=0
   for assignment in employee.salary_components:
    if assignment.deleted_at is not None or not assignment.is_active:continue
    value=float(assignment.amount)*12;component_type=assignment.salary_component.component_type
    if component_type=="bonus":bonus+=value
    elif component_type in{"earning","allowance"}:allowance+=value
   basic=float(employee.basic_salary);result.append({"employee_id":employee.id,"employee_name":f"{employee.first_name} {employee.last_name}".strip(),"basic":basic,"allowances":allowance,"bonus":bonus,"total":basic+allowance+bonus})
  return{"rows":result}
 values=defaultdict(float)
 for employee in staff:
  values["Basic Salary"]+=float(employee.basic_salary)
  for assignment in employee.salary_components:
   if assignment.deleted_at is None and assignment.is_active:values[assignment.salary_component.name]+=float(assignment.amount)*12
 total=sum(values.values());return{"components":[{"name":name,"amount":amount,"percentage":round(amount/total*100,1)if total else 0}for name,amount in values.items()],"rules":[{"name":x.name,"description":x.description,"calculation_type":x.calculation_type,"value":float(x.default_amount)}for x in components()]}
