import random
import sys
from calendar import monthrange
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path

from sqlalchemy.dialects.mysql import insert as mysql_insert

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app import create_app
from app.extensions import db
from app.models import (
    Attendance, Department, Employee, EmployeeSalaryComponent, EmployeeShiftAssignment,
    Event, EventType, Holiday, LeaveRequest, LeaveType, Payroll, PayrollPeriod,
    PerformanceReview, Position, SalaryComponent, Shift, User,
)

RNG = random.Random(20260710)
START = date(2026, 1, 1)
END = date(2026, 7, 10)

NAMES = [
    ("Sok", "Dara"), ("Chan", "Sophea"), ("Chea", "Vannak"), ("Heng", "Sreypov"),
    ("Lim", "Piseth"), ("Kim", "Sotheary"), ("Noun", "Rithy"), ("Ouk", "Sreymom"),
    ("Pech", "Borey"), ("Ros", "Sophal"), ("San", "Sokha"), ("Sin", "Nary"),
    ("Touch", "Makara"), ("Vong", "Sreynich"), ("Yim", "Ratha"), ("Chhay", "Sovann"),
    ("Kea", "Sokunthea"), ("Ly", "Mony"), ("Meas", "Sreyleak"), ("Phan", "Chenda"),
    ("Rin", "Bunna"), ("Sam", "Veasna"), ("Seng", "Davy"), ("Thach", "Sopheap"),
    ("Uk", "Bopha"), ("Van", "Chansokha"), ("Yen", "Sokly"), ("Kong", "Rachana"),
    ("Long", "Vicheka"), ("Mao", "Sreyneang"), ("Nhem", "Kosal"), ("Pov", "Sreypich"),
    ("Sorn", "Panha"), ("Tep", "Sokun"), ("Chhun", "Rady"), ("Em", "Sreymey"),
]

DEPARTMENTS = [
    ("Human Resources", "HR", 180000), ("Engineering", "ENG", 720000),
    ("Finance", "FIN", 360000), ("Sales", "SAL", 420000),
    ("Marketing", "MKT", 300000), ("Operations", "OPS", 480000),
]

POSITIONS = {
    "HR": ["HR Manager", "HR Officer", "Recruitment Specialist"],
    "ENG": ["Engineering Manager", "Software Engineer", "QA Engineer"],
    "FIN": ["Finance Manager", "Accountant", "Payroll Officer"],
    "SAL": ["Sales Manager", "Account Executive", "Sales Associate"],
    "MKT": ["Marketing Manager", "Content Specialist", "Graphic Designer"],
    "OPS": ["Operations Manager", "Operations Officer", "Office Administrator"],
}

HOLIDAYS = [
    (date(2026, 1, 1), "International New Year Day"),
    (date(2026, 1, 7), "Victory over Genocide Day"),
    (date(2026, 3, 8), "International Women's Day"),
    (date(2026, 4, 14), "Khmer New Year - Day 1"),
    (date(2026, 4, 15), "Khmer New Year - Day 2"),
    (date(2026, 4, 16), "Khmer New Year - Day 3"),
    (date(2026, 5, 1), "International Labour Day"),
    (date(2026, 5, 14), "King Norodom Sihamoni's Birthday"),
    (date(2026, 6, 18), "Queen Mother's Birthday"),
]


def one(model, **filters):
    return model.query.filter_by(**filters).first()


def ensure_organization():
    departments = []
    positions = {}
    for name, code, budget in DEPARTMENTS:
        item = one(Department, code=code)
        if not item:
            item = Department(name=name, code=code, description=f"{name} team based in Phnom Penh, Cambodia", annual_budget=budget, is_active=True)
            db.session.add(item)
        else:
            item.name, item.annual_budget, item.is_active = name, budget, True
        departments.append(item)
    db.session.flush()
    for department in departments:
        positions[department.code] = []
        for index, title in enumerate(POSITIONS[department.code]):
            item = Position.query.filter_by(department_id=department.id, title=title).first()
            if not item:
                item = Position(department_id=department.id, title=title, description=f"{title} role in Cambodia", min_salary=350 + index * 150, max_salary=2200 + index * 500, is_active=True)
                db.session.add(item)
            positions[department.code].append(item)
    db.session.flush()
    return departments, positions


def ensure_employees(departments, positions):
    employees = []
    employee_user = one(User, email="employee@example.com")
    for index, (first, last) in enumerate(NAMES, 1):
        code = "EMP-DEMO-001" if index == 1 else f"KH-{index:04d}"
        department = departments[(index - 1) % len(departments)]
        position = positions[department.code][0 if index <= len(departments) else 1 + index % 2]
        employee = one(Employee, employee_code=code)
        salary = Decimal(str(550 + (index % 9) * 125 + (400 if "Manager" in position.title else 0)))
        email = "employee@example.com" if index == 1 else f"{first.lower()}.{last.lower()}@siegecode.com.kh"
        values = dict(
            user_id=employee_user.id if index == 1 and employee_user else None,
            department_id=department.id, position_id=position.id, first_name=first, last_name=last,
            gender="female" if index % 2 == 0 else "male",
            date_of_birth=date(1985 + index % 15, (index % 12) + 1, (index % 26) + 1),
            phone=f"+855 {10 + index % 8}{RNG.randint(1000000, 9999999)}",
            personal_email=f"{first.lower()}.{last.lower()}@gmail.com", work_email=email,
            address=f"Sangkat {['Boeung Keng Kang','Toul Tom Poung','Chroy Changvar','Sen Sok'][index % 4]}, Phnom Penh, Cambodia",
            hire_date=date(2024 + index % 2, (index % 12) + 1, min((index % 25) + 1, 28)),
            employment_status="active", employment_type="full_time", basic_salary=salary,
            bank_name=["ABA Bank", "ACLEDA Bank", "Wing Bank", "Canadia Bank"][index % 4],
            bank_account_name=f"{first} {last}", bank_account_number=f"KH{index:014d}",
            emergency_contact_name=f"{last} Family", emergency_contact_phone=f"+855 9{RNG.randint(1000000,9999999)}",
        )
        if not employee:
            employee = Employee(employee_code=code, **values)
            db.session.add(employee)
        else:
            for key, value in values.items():
                setattr(employee, key, value)
        employees.append(employee)
    db.session.flush()
    if employee_user:
        employee_user.name = "Sok Dara"
    for department in departments:
        manager = next(x for x in employees if x.department_id == department.id and "Manager" in x.position.title)
        department.manager_employee_id = manager.id
        for employee in employees:
            if employee.department_id == department.id and employee.id != manager.id:
                employee.manager_id = manager.id
    db.session.flush()
    return employees


def ensure_shifts(employees):
    definitions = [("Morning Shift", time(8), time(17), "regular"), ("Flexible Shift", time(9), time(18), "flexible"), ("Remote Shift", time(8, 30), time(17, 30), "remote")]
    shifts = []
    for name, start, end, kind in definitions:
        shift = one(Shift, name=name)
        if not shift:
            shift = Shift(name=name, start_time=start, end_time=end, shift_type=kind, status="active", notes="Cambodia office schedule")
            db.session.add(shift)
        shifts.append(shift)
    db.session.flush()
    for index, employee in enumerate(employees):
        assignment = EmployeeShiftAssignment.query.filter_by(employee_id=employee.id, is_active=True).first()
        if not assignment:
            db.session.add(EmployeeShiftAssignment(employee_id=employee.id, shift_id=shifts[index % len(shifts)].id, effective_from=START, is_active=True))
    return shifts


def ensure_holidays():
    for holiday_date, name in HOLIDAYS:
        holiday = one(Holiday, holiday_date=holiday_date)
        if not holiday:
            db.session.add(Holiday(name=name, holiday_date=holiday_date, end_date=holiday_date, is_paid=True, description="Cambodia public holiday"))


def ensure_attendance(employees):
    holidays = {item[0] for item in HOLIDAYS}
    employee_ids = [employee.id for employee in employees]
    existing = set(Attendance.query.with_entities(Attendance.employee_id, Attendance.attendance_date).filter(
        Attendance.employee_id.in_(employee_ids), Attendance.attendance_date.between(START, END)
    ).all())
    day = START
    created = 0
    batch = []
    while day <= END:
        if day.weekday() < 5 and day not in holidays:
            for index, employee in enumerate(employees):
                if employee.hire_date > day or (employee.id, day) in existing:
                    continue
                roll = RNG.random()
                status = "present" if roll < .78 else "remote" if roll < .88 else "late" if roll < .94 else "absent" if roll < .975 else "half_day"
                check_in = check_out = None
                work_minutes = 0
                location = "Phnom Penh Office"
                if status != "absent":
                    minute = RNG.randint(0, 12) if status != "late" else RNG.randint(25, 70)
                    check_in = datetime.combine(day, time(8)) + timedelta(minutes=minute)
                    duration = RNG.randint(450, 540) if status != "half_day" else RNG.randint(210, 270)
                    check_out = check_in + timedelta(minutes=duration)
                    work_minutes = duration
                    if status == "remote":
                        location = "Remote - Cambodia"
                batch.append({"employee_id": employee.id, "attendance_date": day, "check_in": check_in, "check_out": check_out, "work_minutes": work_minutes, "overtime_minutes": max(0, work_minutes - 480), "status": status, "work_location": location, "note": "Generated Cambodia demo activity"})
                created += 1
                if len(batch) >= 500:
                    db.session.execute(mysql_insert(Attendance).prefix_with("IGNORE"), batch)
                    db.session.commit()
                    batch.clear()
        day += timedelta(days=1)
    if batch:
        db.session.execute(mysql_insert(Attendance).prefix_with("IGNORE"), batch)
        db.session.commit()


def ensure_leave(employees, admin):
    leave_types = LeaveType.query.filter(LeaveType.deleted_at.is_(None)).all()
    reasons = ["Family ceremony in Kampong Cham", "Medical appointment", "Visit family in Siem Reap", "Personal business", "Khmer New Year travel"]
    for index, employee in enumerate(employees):
        for offset in (35 + index % 20, 118 + index % 35):
            start = START + timedelta(days=offset)
            while start.weekday() >= 5:
                start += timedelta(days=1)
            days = 1 + index % 3
            end = start + timedelta(days=days - 1)
            if end > END:
                continue
            existing = LeaveRequest.query.filter_by(employee_id=employee.id, start_date=start, end_date=end).first()
            if not existing:
                status = "pending" if index % 8 == 0 and offset > 100 else "approved"
                db.session.add(LeaveRequest(employee_id=employee.id, leave_type_id=leave_types[index % len(leave_types)].id, start_date=start, end_date=end, total_days=days, reason=reasons[index % len(reasons)], status=status, reviewed_by=admin.id if status == "approved" else None, reviewed_at=datetime.combine(start - timedelta(days=3), time(10)) if status == "approved" else None, reviewer_note="Approved for Cambodia demo data" if status == "approved" else None))


def ensure_payroll(employees, admin):
    for month in range(1, 7):
        start = date(2026, month, 1); end = date(2026, month, monthrange(2026, month)[1])
        period = PayrollPeriod.query.filter_by(start_date=start, end_date=end).first()
        if not period:
            period = PayrollPeriod(name=start.strftime("%B 2026"), start_date=start, end_date=end, pay_date=end, status="processed", created_by=admin.id, finalized_by=admin.id, finalized_at=datetime.combine(end, time(16)))
            db.session.add(period); db.session.flush()
        for index, employee in enumerate(employees):
            if one(Payroll, payroll_period_id=period.id, employee_id=employee.id):
                continue
            basic = Decimal(employee.basic_salary); allowance = (basic * Decimal("0.12")).quantize(Decimal("0.01")); bonus = Decimal(str(25 * ((index + month) % 5))); deduction = (basic * Decimal("0.03")).quantize(Decimal("0.01")); tax = (basic * Decimal("0.05")).quantize(Decimal("0.01")); gross = basic + allowance + bonus; net = gross - deduction - tax
            db.session.add(Payroll(payroll_period_id=period.id, employee_id=employee.id, basic_salary=basic, total_allowance=allowance, overtime_pay=0, bonus=bonus, gross_salary=gross, total_deduction=deduction, tax_amount=tax, net_salary=net, payment_status="paid", paid_at=datetime.combine(end, time(15)), payment_reference=f"KH-PAY-2026{month:02d}-{employee.employee_code}"))


def ensure_adjustments(employees, admin):
    component = one(SalaryComponent, code="TRANSPORT_ALLOWANCE")
    if not component:
        return
    for index, employee in enumerate(employees):
        if not EmployeeSalaryComponent.query.filter_by(employee_id=employee.id, salary_component_id=component.id, effective_date=START).first():
            db.session.add(EmployeeSalaryComponent(employee_id=employee.id, salary_component_id=component.id, amount=35 + index % 4 * 10, effective_date=START, is_active=True, status="approved", created_by=admin.id))


def ensure_reviews(employees):
    for index, employee in enumerate(employees):
        reviewer = employee.manager or employees[0]
        if reviewer.id == employee.id:
            reviewer = employees[1]
        for review_date, period_start, period_end in ((date(2026, 4, 5), START, date(2026, 3, 31)), (date(2026, 7, 5), date(2026, 4, 1), date(2026, 6, 30))):
            if not PerformanceReview.query.filter_by(employee_id=employee.id, review_date=review_date).first():
                score = Decimal(str(round(3.5 + ((index * 7 + review_date.month) % 15) / 10, 1)))
                db.session.add(PerformanceReview(employee_id=employee.id, reviewer_id=reviewer.id, review_date=review_date, review_period_start=period_start, review_period_end=period_end, score=score, strengths="Reliable teamwork and strong customer focus", improvements="Continue developing technical and communication skills", comments="Quarterly performance review for Cambodia operations", status="completed"))


def ensure_events(departments, admin):
    types = []
    for name, color in (("Meeting", "indigo"), ("Training", "emerald"), ("Company Event", "amber"), ("Deadline", "rose")):
        item = one(EventType, name=name)
        if not item:
            item = EventType(name=name, color=color); db.session.add(item)
        types.append(item)
    db.session.flush()
    titles = ["Phnom Penh Town Hall", "Quarterly Team Review", "Khmer New Year Celebration", "Customer Service Training", "Cybersecurity Workshop", "Payroll Closing", "Siem Reap Team Retreat", "Operations Planning"]
    locations = ["Phnom Penh HQ", "BKK1 Training Room", "Diamond Island Convention Hall", "Siem Reap Office", "Online - Cambodia"]
    for index in range(24):
        event_date = START + timedelta(days=7 + index * 7)
        if event_date > END:
            break
        title = f"{titles[index % len(titles)]} {event_date.strftime('%b')}"
        if not Event.query.filter_by(title=title, event_date=event_date).first():
            db.session.add(Event(title=title, event_type_id=types[index % len(types)].id, event_date=event_date, start_time=time(9 + index % 6), end_time=time(10 + index % 6, 30), is_all_day=False, location=locations[index % len(locations)], audience_type="all" if index % 3 else "department", department_id=departments[index % len(departments)].id if index % 3 == 0 else None, description="Cambodia team activity and schedule", status="active", created_by=admin.id))


def main():
    app = create_app()
    with app.app_context():
        admin = one(User, email="admin@example.com")
        if not admin:
            raise RuntimeError("Run scripts/seed.py before scripts/seed_demo.py")
        if "--attendance-only" in sys.argv:
            employees = Employee.query.filter(Employee.employee_code.in_(["EMP-DEMO-001"] + [f"KH-{index:04d}" for index in range(2, len(NAMES) + 1)])).order_by(Employee.id).all()
            ensure_attendance(employees)
            print(f"Cambodia attendance ready: {len(employees)} employees, {START} through {END}.")
            return
        departments, positions = ensure_organization()
        employees = ensure_employees(departments, positions)
        ensure_shifts(employees); ensure_holidays(); ensure_leave(employees, admin)
        ensure_payroll(employees, admin); ensure_adjustments(employees, admin)
        ensure_reviews(employees); ensure_events(departments, admin)
        db.session.commit()
        ensure_attendance(employees)
        db.session.commit()
        print(f"Cambodia demo data ready: {len(employees)} employees, {START} through {END}.")


if __name__ == "__main__":
    main()
