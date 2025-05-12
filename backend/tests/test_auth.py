def test_register_user(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"

def test_login_user(client):
    client.post("/auth/register", json={
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "testpassword"
    })
    response = client.post("/auth/login", json={
        "email": "testuser2@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
