from flask import Blueprint, request

from app.api.v1.uploads.service import upload_employee_photo
from app.common.decorators import roles_required
from app.common.responses import error_response, success_response

uploads_bp = Blueprint("uploads", __name__)


@uploads_bp.post("/employees/<int:employee_id>/photo")
@roles_required("Super Admin", "HR Manager")
def employee_photo(employee_id: int):
    data, errors = upload_employee_photo(employee_id, request.files.get("photo"))
    if errors:
        status = 404 if "employee" in errors else 422
        return error_response("Unable to upload employee photo.", status, errors)
    return success_response(data, "Employee photo uploaded")
