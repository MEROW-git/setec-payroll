from app.models import User


def serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.name if user.role else None,
    }


def serialize_auth_result(access_token: str, user: User) -> dict:
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "user": serialize_user(user),
    }
