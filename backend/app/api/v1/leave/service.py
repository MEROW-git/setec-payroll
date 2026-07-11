from datetime import date, datetime, timedelta, timezone

from app.extensions import db
from app.models import Holiday, LeaveGroup, LeavePolicy, LeaveRequest, LeaveType, LeaveYear
from app.api.v1.leave.repository import all_groups,all_holidays,all_policies,all_types,all_years,get_employee,get_request,get_type,list_requests,save
from app.api.v1.leave.schemas import group_data,holiday_data,policy_data,request_data,type_data,year_data


def dashboard(search=""):
    items=[request_data(item) for item in list_requests(search)]; today=date.today(); month=today.strftime("%Y-%m")
    stats={"pending":sum(x["status"]=="pending" for x in items),"approved":sum(x["status"]=="approved" and x["start_date"].startswith(month) for x in items),"rejected":sum(x["status"]=="rejected" and x["start_date"].startswith(month) for x in items),"on_leave_today":sum(x["status"]=="approved" and x["start_date"]<=today.isoformat()<=x["end_date"] for x in items)}
    return {"items":items,"stats":stats}


def create_leave(data):
    employee=get_employee(data["employee_id"]); leave_type=get_type(data["leave_type_id"])
    if not employee:return None,{"employee_id":["Employee was not found."]}
    if not leave_type:return None,{"leave_type_id":["Leave type was not found."]}
    total=(data["end_date"]-data["start_date"]).days+1
    item=save(LeaveRequest(**data,total_days=total,status="pending")); item.employee=employee; item.leave_type=leave_type
    return request_data(item),None


def review_leave(item_id,status,user_id,note=None):
    item=get_request(item_id)
    if not item:return None,{"request":["Leave request was not found."]}
    if item.status!="pending":return None,{"status":["Request has already been reviewed."]}
    item.status=status;item.reviewed_by=user_id;item.reviewed_at=datetime.now(timezone.utc);item.reviewer_note=note;db.session.commit();return request_data(item),None


def configuration_summary():
    today=date.today(); upcoming=today+timedelta(days=30)
    return {"active_policies":sum(x.is_active for x in all_policies()),"upcoming_holidays":sum(today<=x.holiday_date<=upcoming for x in all_holidays()),"pending_adjustments":0}


def list_config(kind):
    mapping={"types":(all_types,type_data),"years":(all_years,year_data),"groups":(all_groups,group_data),"policies":(all_policies,policy_data),"holidays":(all_holidays,holiday_data)}; loader,serializer=mapping[kind];return [serializer(x) for x in loader()]


def create_config(kind,data):
    if kind=="types":
        item=LeaveType(**data); serializer=type_data
    elif kind=="years": item=LeaveYear(**data);serializer=year_data
    elif kind=="groups":
        type_ids=data.pop("leave_type_ids");item=LeaveGroup(**data);item.leave_types=[x for x in all_types() if x.id in type_ids];serializer=group_data
    elif kind=="policies":item=LeavePolicy(**data);serializer=policy_data
    else:item=Holiday(**data);serializer=holiday_data
    try: save(item)
    except Exception:
        db.session.rollback();return None,{"record":["A matching record already exists or the data is invalid."]}
    return serializer(item),None
