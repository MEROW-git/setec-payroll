import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app import create_app
from app.extensions import db
from app.models import LeaveType, Role, SalaryComponent, User
from app.common.security import hash_password

load_dotenv()


ROLES = [
    ("Super Admin", "Full system access"),
    ("HR Manager", "Human resources management access"),
    ("Department Manager", "Department-level management access"),
    ("Employee", "Employee self-service access"),
]

LEAVE_TYPES = [
    ("Annual Leave", "ANNUAL", "Paid annual leave", 18, True, False),
    ("Sick Leave", "SICK", "Paid sick leave", 10, True, True),
    ("Unpaid Leave", "UNPAID", "Unpaid personal leave", 0, False, False),
]

SALARY_COMPONENTS = [
    ("Transport Allowance", "TRANSPORT_ALLOWANCE", "allowance", "fixed", 0, False),
    ("Meal Allowance", "MEAL_ALLOWANCE", "allowance", "fixed", 0, False),
    ("Tax Deduction", "TAX_DEDUCTION", "deduction", "fixed", 0, True),
    ("Late Deduction", "LATE_DEDUCTION", "deduction", "fixed", 0, False),
]


def get_or_create(model, defaults=None, **filters):
    instance = model.query.filter_by(**filters).first()
    if instance:
        return instance, False

    params = {**filters, **(defaults or {})}
    instance = model(**params)
    db.session.add(instance)
    return instance, True


def seed_roles():
    for name, description in ROLES:
        get_or_create(Role, name=name, defaults={"description": description})


def seed_admin():
    admin_name = os.getenv("ADMIN_NAME", "Super Admin")
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        raise RuntimeError("ADMIN_EMAIL and ADMIN_PASSWORD must be set before running seed.py")

    super_admin = Role.query.filter_by(name="Super Admin").first()
    user, created = get_or_create(
        User,
        email=admin_email,
        defaults={
            "role_id": super_admin.id,
            "name": admin_name,
            "password_hash": hash_password(admin_password),
            "is_active": True,
        },
    )
    if not created:
        user.role_id = super_admin.id
        user.name = admin_name
        user.is_active = True


def seed_leave_types():
    for name, code, description, days_per_year, is_paid, requires_attachment in LEAVE_TYPES:
        get_or_create(
            LeaveType,
            code=code,
            defaults={
                "name": name,
                "description": description,
                "days_per_year": days_per_year,
                "is_paid": is_paid,
                "requires_attachment": requires_attachment,
                "is_active": True,
            },
        )


def seed_salary_components():
    for name, code, component_type, calculation_type, default_amount, is_taxable in SALARY_COMPONENTS:
        get_or_create(
            SalaryComponent,
            code=code,
            defaults={
                "name": name,
                "component_type": component_type,
                "calculation_type": calculation_type,
                "default_amount": default_amount,
                "is_taxable": is_taxable,
                "is_active": True,
            },
        )


def main():
    app = create_app()
    with app.app_context():
        seed_roles()
        db.session.flush()
        seed_admin()
        seed_leave_types()
        seed_salary_components()
        db.session.commit()
        print("Seed data inserted.")


if __name__ == "__main__":
    main()
