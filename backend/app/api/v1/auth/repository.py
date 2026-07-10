from sqlalchemy.orm import joinedload

from app.models import User


def get_user_by_email(email: str) -> User | None:
    return (
        User.query.options(joinedload(User.role))
        .filter(User.email == email, User.deleted_at.is_(None))
        .first()
    )


def get_user_by_id(user_id: int) -> User | None:
    return (
        User.query.options(joinedload(User.role))
        .filter(User.id == user_id, User.deleted_at.is_(None))
        .first()
    )
