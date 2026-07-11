def settings_data(user, preference):
    employee = user.employee
    return {
        "profile": {
            "name": user.name,
            "email": user.email,
            "phone": employee.phone if employee else None,
            "job_title": employee.position.title if employee and employee.position else user.role.name if user.role else None,
            "role": user.role.name if user.role else None,
        },
        "appearance": {"theme": preference.theme, "density": preference.density},
        "notifications": {
            "email": preference.email_notifications,
            "push": preference.push_notifications,
            "leave": preference.leave_notifications,
            "payroll": preference.payroll_notifications,
        },
    }
