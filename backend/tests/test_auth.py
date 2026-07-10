def test_login_endpoint_ready(client):
    response = client.post("/api/v1/auth/login")
    assert response.status_code == 422


def test_me_requires_token(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
