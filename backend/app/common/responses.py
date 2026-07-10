from flask import jsonify


def success_response(data=None, message: str = "Success", status_code: int = 200):
    payload = {
        "success": True,
        "message": message,
        "data": data,
    }
    return jsonify(payload), status_code


def error_response(message: str = "Error", status_code: int = 400, errors=None):
    payload = {
        "success": False,
        "message": message,
        "errors": errors,
    }
    return jsonify(payload), status_code
