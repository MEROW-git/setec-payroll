from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models import Department, Employee, PerformanceReview


def list_reviews(search=""):
    query = PerformanceReview.query.options(
        joinedload(PerformanceReview.employee).joinedload(Employee.department),
        joinedload(PerformanceReview.reviewer),
    ).filter(PerformanceReview.deleted_at.is_(None))
    if search:
        pattern = f"%{search}%"
        query = query.join(Employee, PerformanceReview.employee_id == Employee.id).filter(
            or_(Employee.first_name.ilike(pattern), Employee.last_name.ilike(pattern), Employee.employee_code.ilike(pattern))
        )
    return query.order_by(PerformanceReview.review_date.desc()).all()


def active_employee(employee_id):
    return Employee.query.filter(Employee.id == employee_id, Employee.deleted_at.is_(None), Employee.employment_status == "active").first()


def save_review(data):
    review = PerformanceReview(**data)
    db.session.add(review)
    db.session.commit()
    return review


def department_names():
    return Department.query.filter(Department.deleted_at.is_(None), Department.is_active.is_(True)).order_by(Department.name).all()
