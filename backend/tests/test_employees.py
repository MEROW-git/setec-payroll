def test_employee_endpoint_ready(client):
    response = client.get("/api/v1/employees/")
    assert response.status_code == 200
