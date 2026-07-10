def test_payroll_generate_endpoint_ready(client):
    response = client.post("/api/v1/payroll/generate")
    assert response.status_code == 200
