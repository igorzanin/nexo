def test_register_and_login(client):
    # Register
    res = client.post("/api/v1/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data

    # Login
    res = client.post("/api/v1/login", json={
        "username": "testuser",
        "password": "password123",
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data

    # Invalid login
    res = client.post("/api/v1/login", json={
        "username": "testuser",
        "password": "wrong",
    })
    assert res.status_code == 401


def test_register_duplicate(client):
    client.post("/api/v1/register", json={
        "username": "dup", "email": "dup@test.com", "password": "password123",
    })
    res = client.post("/api/v1/register", json={
        "username": "dup", "email": "dup@test.com", "password": "password123",
    })
    assert res.status_code == 409


def test_short_password(client):
    res = client.post("/api/v1/register", json={
        "username": "short", "email": "short@test.com", "password": "123",
    })
    assert res.status_code == 422


def test_refresh_token(client):
    res = client.post("/api/v1/register", json={
        "username": "refresh", "email": "refresh@test.com", "password": "password123",
    })
    tokens = res.json()

    res = client.post("/api/v1/refresh", json={
        "refresh_token": tokens["refresh_token"],
    })
    assert res.status_code == 200
    assert "access_token" in res.json()
