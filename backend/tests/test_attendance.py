def test_attendance_history_endpoint_ready(client):
    response = client.get("/api/v1/attendance/history")
    assert response.status_code == 200
