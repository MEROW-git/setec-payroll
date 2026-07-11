from decimal import Decimal
def calculate_tax(income,rules):
 income=Decimal(income);tax=Decimal("0")
 for rule in rules:
  lower=Decimal(rule.min_income);upper=Decimal(rule.max_income)if rule.max_income is not None else income
  taxable=max(Decimal("0"),min(income,upper)-lower)
  tax+=taxable*Decimal(rule.rate)/Decimal("100")
 return max(Decimal("0"),tax)
def calculate_employee(employee,start,end,tax_rules):
 basic=Decimal(employee.basic_salary)/Decimal("12");allowance=deduction=bonus=Decimal("0")
 for assignment in employee.salary_components:
  if assignment.deleted_at is not None or assignment.status!="approved"or assignment.effective_date>end or(assignment.end_date and assignment.end_date<start):continue
  amount=Decimal(assignment.amount);kind=assignment.salary_component.component_type
  if kind in{"earning","allowance"}:allowance+=amount
  elif kind=="bonus":bonus+=amount
  else:deduction+=amount
 gross=basic+allowance+bonus;tax=calculate_tax(gross,tax_rules);net=max(Decimal("0"),gross-deduction-tax)
 return{"basic_salary":basic,"total_allowance":allowance,"overtime_pay":0,"bonus":bonus,"gross_salary":gross,"total_deduction":deduction,"tax_amount":tax,"net_salary":net,"payment_status":"unpaid"}
