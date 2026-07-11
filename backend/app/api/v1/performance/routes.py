from flask import Blueprint, request

from app.api.v1.performance.service import create_review, dashboard
from app.api.v1.performance.validators import validate_review
from app.common.decorators import roles_required
from app.common.responses import error_response, success_response

performance_bp = Blueprint("performance", __name__)


@performance_bp.get("/")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def get_dashboard():
    return success_response(dashboard((request.args.get("search") or "").strip()), "Performance reviews loaded")


@performance_bp.post("/")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def create():
    validation = validate_review(request.get_json(silent=True) or {})
    if not validation["is_valid"]: return error_response("Invalid assessment data.", 422, validation["errors"])
    item, errors = create_review(validation["data"])
    if errors: return error_response("Unable to create assessment.", 422, errors)
    return success_response(item, "Assessment created", 201)
