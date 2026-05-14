def test_add_and_remove_member(client):
    res = client.post("/api/v1/register", json={
        "username": "admin", "email": "admin@test.com", "password": "password123",
    })
    token1 = res.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    res = client.post("/api/v1/register", json={
        "username": "user", "email": "user@test.com", "password": "password123",
    })
    data2 = res.json()
    user2_id = ""
    headers2 = {"Authorization": f"Bearer {data2['access_token']}"}

    res = client.post("/api/v1/teams", json={"title": "Team", "signupToken": ""}, headers=headers1)
    team_id = res.json()["id"]

    res = client.post("/api/v1/boards", json={"team_id": team_id, "title": "Board"}, headers=headers1)
    board_id = res.json()["id"]

    # Get members
    res = client.get(f"/api/v1/boards/{board_id}/members", headers=headers1)
    assert res.status_code == 200
    admin_id = res.json()[0]["userId"]

    # Second user registers
    res = client.post("/api/v1/register", json={
        "username": "member2", "email": "member2@test.com", "password": "password123",
    })
    assert res.status_code == 200
    member2_id = res.json()["access_token"]

    # Get member2's user ID from a GET /teams
    res = client.get("/api/v1/teams", headers={"Authorization": f"Bearer {member2_id}"})
    assert res.status_code == 200

    # Find member2 user id by decoding token
    from nexo.auth.jwt import decode_token
    payload = decode_token(member2_id)
    assert payload and payload.get("sub")

    # Add member2 as editor
    res = client.post(f"/api/v1/boards/{board_id}/members", json={
        "boardId": board_id, "userId": payload["sub"],
        "minimumRole": "", "schemeAdmin": False, "schemeEditor": True,
        "schemeCommenter": False, "schemeViewer": False,
    }, headers=headers1)
    assert res.status_code == 200
