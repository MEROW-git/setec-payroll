def review_data(review):
    employee = review.employee
    reviewer = review.reviewer
    return {
        "id": review.id,
        "employee_id": review.employee_id,
        "employee_name": f"{employee.first_name} {employee.last_name}".strip(),
        "employee_code": employee.employee_code,
        "department": employee.department.name if employee.department else None,
        "reviewer_id": review.reviewer_id,
        "reviewer_name": f"{reviewer.first_name} {reviewer.last_name}".strip(),
        "review_date": review.review_date.isoformat(),
        "period_start": review.review_period_start.isoformat() if review.review_period_start else None,
        "period_end": review.review_period_end.isoformat() if review.review_period_end else None,
        "score": float(review.score) if review.score is not None else None,
        "strengths": review.strengths,
        "improvements": review.improvements,
        "comments": review.comments,
        "status": review.status,
    }
