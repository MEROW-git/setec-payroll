from datetime import date


def parse_date(value,field,errors):
    try:return date.fromisoformat(value)
    except (TypeError,ValueError):errors[field]=[f"{field.replace('_',' ').title()} is required."];return None


def request_payload(payload):
    errors={};data={"reason":(payload.get("reason")or"").strip()or None}
    for field in("employee_id","leave_type_id"):
        try:data[field]=int(payload.get(field))
        except(TypeError,ValueError):errors[field]=[f"{field.replace('_',' ').title()} is required."]
    data["start_date"]=parse_date(payload.get("start_date"),"start_date",errors);data["end_date"]=parse_date(payload.get("end_date"),"end_date",errors)
    if data["start_date"]and data["end_date"]and data["end_date"]<data["start_date"]:errors["end_date"]=["End date cannot be before start date."]
    return {"is_valid":not errors,"errors":errors,"data":data}


def config_payload(kind,payload):
    errors={}
    if kind=="types":
        name=(payload.get("name")or"").strip();data={"name":name,"code":(payload.get("code")or name.upper().replace(" ","_")[:30]),"description":None,"days_per_year":float(payload.get("days_per_year")or 0),"is_paid":bool(payload.get("is_paid",True)),"requires_attachment":False,"is_active":True,"count_type":payload.get("count_type")or"daily","special_types":payload.get("special_types")or[]}
        if not name:errors["name"]=["Leave type name is required."]
    elif kind=="years":
        try:year=int(payload.get("year"))
        except(TypeError,ValueError):year=0;errors["year"]=["Year is required."]
        data={"year":year,"start_date":parse_date(payload.get("start_date"),"start_date",errors),"end_date":parse_date(payload.get("end_date"),"end_date",errors),"status":payload.get("status")or"active"}
    elif kind=="groups":
        data={"name":(payload.get("name")or"").strip(),"leave_type_ids":[int(x)for x in payload.get("leave_type_ids",[])]}
        if not data["name"]:errors["name"]=["Group name is required."]
        if not data["leave_type_ids"]:errors["leave_type_ids"]=["Select at least one leave type."]
    elif kind=="policies":
        data={"name":(payload.get("name")or"").strip(),"count_type":payload.get("count_type")or"daily","considerable_hours":float(payload.get("considerable_hours")or 0),"adjusted_days":float(payload.get("adjusted_days")or 0),"description":(payload.get("description")or"").strip()or None,"is_active":True}
        if not data["name"]:errors["name"]=["Policy name is required."]
    else:
        data={"name":(payload.get("name")or"").strip(),"description":(payload.get("description")or"").strip()or None,"holiday_date":parse_date(payload.get("start_date"),"start_date",errors),"end_date":parse_date(payload.get("end_date"),"end_date",errors),"department_id":int(payload["department_id"])if payload.get("department_id")else None,"is_paid":True}
        if not data["name"]:errors["name"]=["Holiday name is required."]
    return {"is_valid":not errors,"errors":errors,"data":data}
