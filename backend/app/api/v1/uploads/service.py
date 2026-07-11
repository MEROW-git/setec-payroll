import cloudinary
import cloudinary.uploader
from flask import current_app
from werkzeug.datastructures import FileStorage

from app.api.v1.uploads.repository import get_employee, save_profile_photo

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024


def upload_employee_photo(employee_id: int, image: FileStorage | None) -> tuple[dict | None, dict | None]:
    employee = get_employee(employee_id)
    if not employee:
        return None, {"employee": ["Employee was not found."]}
    if not image or not image.filename:
        return None, {"photo": ["Select an image to upload."]}
    if image.mimetype not in ALLOWED_IMAGE_TYPES:
        return None, {"photo": ["Photo must be a JPEG, PNG, or WebP image."]}

    image.stream.seek(0, 2)
    size = image.stream.tell()
    image.stream.seek(0)
    if size > MAX_IMAGE_BYTES:
        return None, {"photo": ["Photo must not exceed 5 MB."]}

    config = current_app.config
    if not all((config["CLOUDINARY_CLOUD_NAME"], config["CLOUDINARY_API_KEY"], config["CLOUDINARY_API_SECRET"])):
        return None, {"cloudinary": ["Cloudinary is not configured."]}
    cloudinary.config(
        cloud_name=config["CLOUDINARY_CLOUD_NAME"],
        api_key=config["CLOUDINARY_API_KEY"],
        api_secret=config["CLOUDINARY_API_SECRET"],
        secure=True,
    )
    try:
        result = cloudinary.uploader.upload(
            image.stream,
            resource_type="image",
            public_id=f"hrm/employees/employee_{employee.id}",
            overwrite=True,
            invalidate=True,
            unique_filename=False,
            transformation=[{"width": 1200, "height": 1200, "crop": "limit", "quality": "auto"}],
            tags=["hrm", "employee-profile"],
        )
    except Exception:
        current_app.logger.exception("Cloudinary employee photo upload failed", extra={"employee_id": employee.id})
        return None, {"photo": ["Photo storage is temporarily unavailable."]}

    secure_url = result.get("secure_url")
    if not secure_url:
        return None, {"photo": ["Cloudinary did not return a secure image URL."]}
    save_profile_photo(employee, secure_url)
    return {
        "employee_id": employee.id,
        "profile_photo": secure_url,
        "public_id": result.get("public_id"),
        "width": result.get("width"),
        "height": result.get("height"),
        "format": result.get("format"),
        "bytes": result.get("bytes"),
    }, None
