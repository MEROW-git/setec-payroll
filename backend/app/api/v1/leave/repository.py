from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models import Employee, Holiday, LeaveGroup, LeavePolicy, LeaveRequest, LeaveType, LeaveYear


def list_requests(search=""):
    query = LeaveRequest.query.options(joinedload(LeaveRequest.employee), joinedload(LeaveRequest.leave_type)).filter(LeaveRequest.deleted_at.is_(None))
    if search:
        pattern=f"%{search}%"; query=query.join(Employee).filter(or_(Employee.first_name.ilike(pattern),Employee.last_name.ilike(pattern)))
    return query.order_by(LeaveRequest.created_at.desc()).all()


def get_request(item_id): return LeaveRequest.query.options(joinedload(LeaveRequest.employee),joinedload(LeaveRequest.leave_type)).filter(LeaveRequest.id==item_id,LeaveRequest.deleted_at.is_(None)).first()
def get_employee(item_id): return Employee.query.filter(Employee.id==item_id,Employee.deleted_at.is_(None)).first()
def get_type(item_id): return LeaveType.query.filter(LeaveType.id==item_id,LeaveType.deleted_at.is_(None),LeaveType.is_active.is_(True)).first()
def save(model): db.session.add(model); db.session.commit(); return model
def all_types(): return LeaveType.query.filter(LeaveType.deleted_at.is_(None)).order_by(LeaveType.name).all()
def all_years(): return LeaveYear.query.filter(LeaveYear.deleted_at.is_(None)).order_by(LeaveYear.year.desc()).all()
def all_groups(): return LeaveGroup.query.options(joinedload(LeaveGroup.leave_types)).filter(LeaveGroup.deleted_at.is_(None)).order_by(LeaveGroup.name).all()
def all_policies(): return LeavePolicy.query.filter(LeavePolicy.deleted_at.is_(None)).order_by(LeavePolicy.created_at.desc()).all()
def all_holidays(): return Holiday.query.options(joinedload(Holiday.department)).order_by(Holiday.holiday_date.desc()).all()
def find_unique(model, field, value): return model.query.filter(field==value,model.deleted_at.is_(None)).first()
