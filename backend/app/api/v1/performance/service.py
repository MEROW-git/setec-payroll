from collections import defaultdict

from app.api.v1.performance.repository import active_employee, department_names, list_reviews, save_review
from app.api.v1.performance.schemas import review_data


def dashboard(search=""):
    reviews = list_reviews(search)
    completed = [review for review in reviews if review.status == "completed" and review.score is not None]
    employee_ids = {review.employee_id for review in completed}
    scores = [float(review.score) for review in completed]
    departments = defaultdict(list)
    for review in completed:
        departments[review.employee.department.name if review.employee.department else "Unassigned"].append(float(review.score))
    return {
        "items": [review_data(review) for review in reviews],
        "stats": {
            "average_score": round(sum(scores) / len(scores), 2) if scores else 0,
            "completed": len(completed),
            "drafts": sum(review.status == "draft" for review in reviews),
            "employees_reviewed": len(employee_ids),
        },
        "departments": [
            {"name": department.name, "average_score": round(sum(departments[department.name]) / len(departments[department.name]), 2) if departments[department.name] else 0, "review_count": len(departments[department.name])}
            for department in department_names()
        ],
    }


def create_review(data):
    employee = active_employee(data["employee_id"])
    reviewer = active_employee(data["reviewer_id"])
    if not employee or not reviewer: return None, {"employee": ["Employee or reviewer was not found."]}
    if employee.id == reviewer.id: return None, {"reviewer_id": ["An employee cannot review themselves."]}
    model_data = {key: value for key, value in data.items() if key not in {"period_start", "period_end"}}
    model_data["review_period_start"] = data["period_start"]
    model_data["review_period_end"] = data["period_end"]
    return review_data(save_review(model_data)), None
