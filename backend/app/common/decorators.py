from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.api.v1.auth.repository import get_user_by_id
from app.common.responses import error_response


def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = get_user_by_id(int(user_id)) if user_id else None

            if not user or not user.is_active:
                return error_response("Authentication required.", status_code=401)

            role_name = user.role.name if user.role else None
            if roles and role_name not in roles:
                return error_response("You do not have permission to perform this action.", status_code=403)

            return fn(*args, **kwargs)

        return wrapper

    return decorator
