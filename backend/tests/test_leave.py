def test_leave_apply_endpoint_ready(client):
    response = client.post("/api/v1/leave/")
    assert response.status_code == 200
