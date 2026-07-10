from app.models import Department


def list_active_departments() -> list[Department]:
    return (
        Department.query.filter(
            Department.deleted_at.is_(None),
            Department.is_active.is_(True),
        )
        .order_by(Department.name.asc())
        .all()
    )
