from flask import Blueprint, request

from app.api.v1.positions.service import get_positions
from app.common.decorators import roles_required
from app.common.responses import success_response

positions_bp = Blueprint("positions", __name__)


@positions_bp.get("/")
@roles_required("Super Admin", "HR Manager", "Department Manager")
def list_positions():
    return success_response(
        data=get_positions(department_id=(request.args.get("department_id") or "").strip()),
        message="Positions loaded",
    )
