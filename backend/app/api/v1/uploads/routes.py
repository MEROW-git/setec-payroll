from flask import Blueprint

from app.common.responses import success_response

uploads_bp = Blueprint("uploads", __name__)


@uploads_bp.post("/")
def upload_file():
    return success_response(message="Upload endpoint ready")
