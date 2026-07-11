from datetime import date
def validate_entry(payload):
    errors={};kind=(payload.get("adjustment_type")or"").strip();status=(payload.get("status")or"approved").strip();category=(payload.get("category")or"").strip()
    try:employee_id=int(payload.get("employee_id"))
    except(TypeError,ValueError):employee_id=None;errors["employee_id"]=["Employee is required."]
    try:amount=float(payload.get("amount"));assert amount>0
    except(TypeError,ValueError,AssertionError):amount=0;errors["amount"]=["Amount must be greater than zero."]
    try:effective_date=date.fromisoformat(payload.get("date"))
    except(TypeError,ValueError):effective_date=None;errors["date"]=["Adjustment date is required."]
    if kind not in{"allowance","deduction"}:errors["adjustment_type"]=["Adjustment type is invalid."]
    if status not in{"pending","approved","rejected"}:errors["status"]=["Status is invalid."]
    if not category:errors["category"]=["Category or reason is required."]
    return{"is_valid":not errors,"errors":errors,"data":{"employee_id":employee_id,"amount":amount,"effective_date":effective_date,"end_date":None,"is_active":status=="approved","status":status},"category":category,"kind":kind}
