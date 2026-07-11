from datetime import date

from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models import Employee, EmployeeShiftAssignment, Shift, ShiftRequest


def list_shifts(search: str = ""):
    query = db.session.query(Shift, func.count(EmployeeShiftAssignment.id)).outerjoin(
        EmployeeShiftAssignment,
        (EmployeeShiftAssignment.shift_id == Shift.id) & EmployeeShiftAssignment.is_active.is_(True),
    ).filter(Shift.deleted_at.is_(None)).group_by(Shift.id)
    if search:
        query = query.filter(Shift.name.ilike(f"%{search}%"))
    return query.order_by(Shift.start_time.asc()).all()


def get_shift(shift_id: int) -> Shift | None:
    return Shift.query.filter(Shift.id == shift_id, Shift.deleted_at.is_(None)).first()


def get_shift_by_name(name: str) -> Shift | None:
    return Shift.query.filter(func.lower(Shift.name) == name.lower(), Shift.deleted_at.is_(None)).first()


def create_shift(data: dict) -> Shift:
    shift = Shift(**data)
    db.session.add(shift); db.session.commit(); return shift


def list_requests(search: str = "") -> list[ShiftRequest]:
    query = ShiftRequest.query.options(joinedload(ShiftRequest.requester), joinedload(ShiftRequest.target_employee), joinedload(ShiftRequest.current_shift), joinedload(ShiftRequest.new_shift))
    if search:
        pattern = f"%{search}%"
        query = query.join(Employee, ShiftRequest.requester_id == Employee.id).filter(or_(Employee.first_name.ilike(pattern), Employee.last_name.ilike(pattern)))
    return query.order_by(ShiftRequest.created_at.desc()).all()


def get_request(request_id: int) -> ShiftRequest | None:
    return ShiftRequest.query.options(joinedload(ShiftRequest.requester), joinedload(ShiftRequest.target_employee), joinedload(ShiftRequest.current_shift), joinedload(ShiftRequest.new_shift)).filter(ShiftRequest.id == request_id).first()


def create_request(data: dict) -> ShiftRequest:
    item = ShiftRequest(**data); db.session.add(item); db.session.commit(); return get_request(item.id)


def get_employee(employee_id: int) -> Employee | None:
    return Employee.query.filter(Employee.id == employee_id, Employee.deleted_at.is_(None)).first()


def active_assignment(employee_id: int) -> EmployeeShiftAssignment | None:
    return EmployeeShiftAssignment.query.filter_by(employee_id=employee_id, is_active=True).first()


def set_assignment(employee_id: int, shift_id: int, effective_from: date):
    current = active_assignment(employee_id)
    if current:
        current.is_active = False; current.effective_to = effective_from
    db.session.add(EmployeeShiftAssignment(employee_id=employee_id, shift_id=shift_id, effective_from=effective_from, is_active=True))


def finalize_request(item: ShiftRequest, status: str, reviewer_id: int):
    from datetime import datetime, timezone
    if status == "approved":
        if item.request_type == "change":
            set_assignment(item.requester_id, item.new_shift_id, item.request_date)
        else:
            target_assignment = active_assignment(item.target_employee_id)
            set_assignment(item.requester_id, target_assignment.shift_id if target_assignment else item.current_shift_id, item.request_date)
            set_assignment(item.target_employee_id, item.current_shift_id, item.request_date)
    item.status = status; item.reviewed_by = reviewer_id; item.reviewed_at = datetime.now(timezone.utc)
    db.session.commit()
