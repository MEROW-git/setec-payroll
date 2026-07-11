from calendar import monthrange
from datetime import date
from app.api.v1.adjustments.repository import get_employee,list_entries,save_entry
from app.api.v1.adjustments.schemas import entry_data

def month_range(month):
    year,number=map(int,month.split("-"));return date(year,number,1),date(year,number,monthrange(year,number)[1])
def get_adjustments(month,search="",component_type="",status=""):
    start,end=month_range(month);items=[entry_data(x)for x in list_entries(start,end,search,component_type,status)];allowances=sum(x["amount"]for x in items if x["adjustment_type"]=="allowance"and x["status"]=="approved");deductions=sum(x["amount"]for x in items if x["adjustment_type"]=="deduction"and x["status"]=="approved");return{"items":items,"stats":{"allowances":allowances,"deductions":deductions,"net":allowances-deductions},"month":month}
def create_adjustment(data,category,kind,user_id):
    if not get_employee(data["employee_id"]):return None,{"employee_id":["Employee was not found."]}
    data["created_by"]=user_id;return entry_data(save_entry(data,category,kind)),None
