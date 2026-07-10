from flask import Blueprint

from app.common.responses import success_response

positions_bp = Blueprint("positions", __name__)


@positions_bp.get("/")
def list_positions():
    return success_response(data=[], message="Position endpoints ready")
