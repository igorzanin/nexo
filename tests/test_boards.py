def test_create_board(client):
    # Register
    res = client.post("/api/v1/register", json={
        "username": "boardtest", "email": "board@test.com", "password": "password123",
    })
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create team first
    res = client.post("/api/v1/teams", json={"title": "Test Team", "signupToken": ""}, headers=headers)
    team_id = res.json()["id"]

    # Create board
    res = client.post("/api/v1/boards", json={
        "team_id": team_id,
        "title": "Test Board",
        "type": "P",
    }, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Test Board"
    assert data["type"] == "P"
    board_id = data["id"]

    # Get board
    res = client.get(f"/api/v1/boards/{board_id}", headers=headers)
    assert res.status_code == 200
    assert res.json()["title"] == "Test Board"

    # Get boards by team
    res = client.get(f"/api/v1/teams/{team_id}/boards", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Patch board
    res = client.patch(f"/api/v1/boards/{board_id}", json={"title": "Updated"}, headers=headers)
    assert res.status_code == 200
    assert res.json()["title"] == "Updated"

    # Delete board
    res = client.delete(f"/api/v1/boards/{board_id}", headers=headers)
    assert res.status_code == 204


def test_board_permissions(client):
    res = client.post("/api/v1/register", json={
        "username": "owner", "email": "owner@test.com", "password": "password123",
    })
    token1 = res.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    res = client.post("/api/v1/teams", json={"title": "Team", "signupToken": ""}, headers=headers1)
    team_id = res.json()["id"]

    res = client.post("/api/v1/boards", json={"team_id": team_id, "title": "Private"}, headers=headers1)
    board_id = res.json()["id"]

    # Second user tries to access
    res = client.post("/api/v1/register", json={
        "username": "intruder", "email": "intruder@test.com", "password": "password123",
    })
    token2 = res.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    res = client.get(f"/api/v1/boards/{board_id}", headers=headers2)
    assert res.status_code == 200
