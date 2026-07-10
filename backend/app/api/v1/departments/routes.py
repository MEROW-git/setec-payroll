from flask import Blueprint

from app.api.v1.departments.service import get_departments
from app.common.decorators import roles_required
from app.common.responses import success_response

departments_bp = Blueprint("departments", __name__)


@departments_bp.get("/")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def list_departments():
    return success_response(data=get_departments(), message="Departments loaded")
