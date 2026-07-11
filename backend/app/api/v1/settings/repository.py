from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models import Employee, User, UserPreference


def user_settings(user_id):
    return User.query.options(joinedload(User.role), joinedload(User.employee).joinedload(Employee.position), joinedload(User.preference)).filter(User.id == user_id, User.deleted_at.is_(None)).first()


def email_in_use(email, user_id):
    return User.query.filter(User.email == email, User.id != user_id, User.deleted_at.is_(None)).first() is not None


def ensure_preference(user):
    if not user.preference:
        user.preference = UserPreference(user_id=user.id)
        db.session.add(user.preference)
        db.session.commit()
    return user.preference


def commit():
    db.session.commit()
