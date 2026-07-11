def config_payload(kind,payload):
 errors={}
 try:
  if kind=="components":
   name=(payload.get("name")or"").strip();data={"name":name,"code":(payload.get("code")or name.upper().replace(" ","_")[:50]),"component_type":payload.get("component_type")or"earning","calculation_type":payload.get("calculation_type")or"fixed","default_amount":float(payload.get("value")or 0),"is_taxable":bool(payload.get("is_taxable",False)),"is_active":True,"description":(payload.get("description")or"").strip()or None}
   if not name:errors["name"]=["Component name is required."]
  elif kind=="cycles":
   data={"name":(payload.get("name")or"").strip(),"frequency":payload.get("frequency")or"monthly","pay_day":int(payload.get("pay_day")or 1),"is_default":bool(payload.get("is_default",False)),"is_active":True}
   if not data["name"]:errors["name"]=["Cycle name is required."]
  elif kind=="taxes":data={"min_income":float(payload.get("min_income")or 0),"max_income":float(payload["max_income"])if payload.get("max_income")not in(None,"")else None,"rate":float(payload.get("rate")or 0),"description":(payload.get("description")or"").strip()or None,"is_active":True}
  else:
   data={"name":(payload.get("name")or"").strip(),"category":payload.get("category")or"deduction","count_type":payload.get("count_type")or"daily","policy_type":payload.get("policy_type")or"regular","considerable_value":float(payload.get("considerable_value")or 0),"adjusted_value":float(payload.get("adjusted_value")or 0),"value_mode":payload.get("value_mode")or"amount","description":(payload.get("description")or"").strip()or None,"is_active":True}
   if not data["name"]:errors["name"]=["Policy name is required."]
 except(TypeError,ValueError):data={};errors["values"]=["Numeric values are invalid."]
 return{"is_valid":not errors,"errors":errors,"data":data}
