from flask_jwt_extended import create_access_token

from app.api.v1.auth.repository import get_user_by_email, get_user_by_id
from app.api.v1.auth.schemas import serialize_auth_result, serialize_user
from app.common.security import verify_password


def authenticate_user(email: str, password: str) -> dict | None:
    user = get_user_by_email(email)
    if not user or not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    access_token = create_access_token(identity=str(user.id))
    return serialize_auth_result(access_token=access_token, user=user)


def get_current_user_profile(user_id: str) -> dict | None:
    try:
        parsed_user_id = int(user_id)
    except (TypeError, ValueError):
        return None

    user = get_user_by_id(parsed_user_id)
    if not user or not user.is_active:
        return None

    return serialize_user(user)
