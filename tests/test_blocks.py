def test_create_block(client):
    res = client.post("/api/v1/register", json={
        "username": "blocktest", "email": "block@test.com", "password": "password123",
    })
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.post("/api/v1/teams", json={"title": "Team", "signupToken": ""}, headers=headers)
    team_id = res.json()["id"]

    res = client.post("/api/v1/boards", json={"team_id": team_id, "title": "Board"}, headers=headers)
    board_id = res.json()["id"]

    # Create block
    res = client.post(f"/api/v1/boards/{board_id}/blocks", json={
        "board_id": board_id,
        "type": "text",
        "title": "Hello World",
    }, headers=headers)
    assert res.status_code == 200
    block_id = res.json()["id"]

    # Get blocks
    res = client.get(f"/api/v1/boards/{board_id}/blocks", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Patch block
    res = client.patch(f"/api/v1/boards/{board_id}/blocks/{block_id}", json={
        "title": "Updated",
    }, headers=headers)
    assert res.status_code == 200

    # Delete block
    res = client.delete(f"/api/v1/boards/{board_id}/blocks/{block_id}", headers=headers)
    assert res.status_code == 204


def test_create_card(client):
    res = client.post("/api/v1/register", json={
        "username": "cardtest", "email": "card@test.com", "password": "password123",
    })
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.post("/api/v1/teams", json={"title": "Team", "signupToken": ""}, headers=headers)
    team_id = res.json()["id"]

    res = client.post("/api/v1/boards", json={"team_id": team_id, "title": "Board"}, headers=headers)
    board_id = res.json()["id"]

    # Create card
    res = client.post(f"/api/v1/boards/{board_id}/cards", json={
        "board_id": board_id,
        "type": "card",
        "title": "Test Card",
    }, headers=headers)
    assert res.status_code == 200
    card_id = res.json()["id"]

    # Get cards
    res = client.get(f"/api/v1/boards/{board_id}/cards", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Get single card
    res = client.get(f"/api/v1/cards/{card_id}", headers=headers)
    assert res.status_code == 200
    assert res.json()["title"] == "Test Card"
