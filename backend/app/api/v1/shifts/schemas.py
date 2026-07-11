def serialize_shift(shift, employee_count=0):
    return {"id": shift.id, "name": shift.name, "start_time": shift.start_time.strftime("%H:%M"), "end_time": shift.end_time.strftime("%H:%M"), "shift_type": shift.shift_type, "status": shift.status, "notes": shift.notes, "employee_count": employee_count}


def serialize_request(item):
    return {"id": item.id, "request_type": item.request_type, "request_date": item.request_date.isoformat(), "requester_id": item.requester_id, "requester_name": f"{item.requester.first_name} {item.requester.last_name}".strip(), "current_shift_id": item.current_shift_id, "current_shift": item.current_shift.name, "target_employee_id": item.target_employee_id, "target_employee_name": f"{item.target_employee.first_name} {item.target_employee.last_name}".strip() if item.target_employee else None, "new_shift_id": item.new_shift_id, "new_shift": item.new_shift.name if item.new_shift else None, "remarks": item.remarks, "status": item.status, "created_at": item.created_at.isoformat()}
