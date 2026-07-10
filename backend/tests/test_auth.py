def test_login_endpoint_ready(client):
    response = client.post("/api/v1/auth/login")
    assert response.status_code == 200
