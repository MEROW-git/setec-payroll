from datetime import date,time
def event_payload(payload):
 errors={};data={"title":(payload.get("title")or"").strip(),"location":(payload.get("location")or"").strip(),"description":(payload.get("description")or"").strip()or None,"audience_type":"department"if payload.get("department_id")else"all","department_id":int(payload["department_id"])if payload.get("department_id")else None,"status":"active","is_all_day":bool(payload.get("is_all_day",False))}
 for field in("title","location"):
  if not data[field]:errors[field]=[f"{field.title()} is required."]
 try:data["event_type_id"]=int(payload.get("event_type_id"))
 except(TypeError,ValueError):errors["event_type_id"]=["Event type is required."]
 try:data["event_date"]=date.fromisoformat(payload.get("date"))
 except(TypeError,ValueError):errors["date"]=["Event date is required."]
 for field in("start_time","end_time"):
  try:data[field]=time.fromisoformat(payload.get(field))if payload.get(field)else None
  except ValueError:errors[field]=[f"{field.replace('_',' ').title()} is invalid."]
 return{"is_valid":not errors,"errors":errors,"data":data}
def notice_payload(payload):
 errors={};data={"title":(payload.get("title")or"").strip(),"content":(payload.get("content")or"").strip(),"priority":payload.get("priority")or"medium","status":payload.get("status")or"active","audience_type":"department"if payload.get("department_id")else"all","department_id":int(payload["department_id"])if payload.get("department_id")else None}
 for field in("title","content"):
  if not data[field]:errors[field]=[f"{field.title()} is required."]
 try:data["notice_date"]=date.fromisoformat(payload.get("date"))
 except(TypeError,ValueError):errors["date"]=["Notice date is required."]
 return{"is_valid":not errors,"errors":errors,"data":data}
