"""Integration tests — BC-Collaboration sharing (PT-005 / BR-HUMANA-001).

Cobre os cenários de readToken per BR-HUMANA-001:
- Geração de token ao habilitar sharing
- Acesso público com token válido retorna o board
- Acesso com token inválido retorna 404
- Acesso quando sharing está desabilitado retorna 404
- Revogar sharing (DELETE) torna board inacessível publicamente
- Subscriptions CRUD (criar, listar, deletar)
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from nexo.db.base import Base
from nexo.db.session import get_db
from nexo.main import app

TEST_DB_URL = "sqlite:///./test_sharing.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    from limits.storage import MemoryStorage
    app.state.limiter._limiter.storage = MemoryStorage()
    yield


@pytest.fixture(scope="module")
def client():
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


@pytest.fixture(scope="module")
def auth_headers(client: TestClient):
    res = client.post("/api/v1/register", json={
        "username": "sharinguser", "email": "sharing@test.com", "password": "password123",
    })
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def board_id(client: TestClient, auth_headers: dict):
    res = client.post("/api/v1/teams", json={"title": "Sharing Team", "signupToken": ""}, headers=auth_headers)
    team_id = res.json()["id"]
    res = client.post("/api/v1/boards", json={"team_id": team_id, "title": "Shared Board", "type": "O"}, headers=auth_headers)
    return res.json()["id"]


class TestSharingTokenGeneration:
    def test_enable_sharing_generates_token(self, client, auth_headers, board_id):
        res = client.post(f"/api/v1/boards/{board_id}/sharing",
                          json={"enabled": True},
                          headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["enabled"] is True
        assert len(data["token"]) > 10  # auto-generated token

    def test_get_sharing_returns_token(self, client, auth_headers, board_id):
        res = client.get(f"/api/v1/boards/{board_id}/sharing", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["token"]

    def test_update_sharing_with_custom_token(self, client, auth_headers, board_id):
        res = client.post(f"/api/v1/boards/{board_id}/sharing",
                          json={"enabled": True, "token": "my-custom-token-123"},
                          headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["token"] == "my-custom-token-123"


class TestPublicBoardAccess:
    @pytest.fixture(scope="class")
    def read_token(self, client, auth_headers, board_id):
        """Enable sharing and return the read token."""
        res = client.post(f"/api/v1/boards/{board_id}/sharing",
                          json={"enabled": True},
                          headers=auth_headers)
        return res.json()["token"]

    def test_valid_token_returns_board(self, client, board_id, read_token):
        """Public access with valid readToken — no auth header."""
        res = client.get(f"/api/v1/shared/boards/{read_token}")
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == board_id

    def test_invalid_token_returns_404(self, client):
        res = client.get("/api/v1/shared/boards/totally-invalid-token-xyz")
        assert res.status_code == 404

    def test_disabled_sharing_returns_404(self, client, auth_headers, board_id, read_token):
        """Disable sharing — public access should fail."""
        client.post(f"/api/v1/boards/{board_id}/sharing",
                    json={"enabled": False, "token": read_token},
                    headers=auth_headers)
        res = client.get(f"/api/v1/shared/boards/{read_token}")
        assert res.status_code == 404

    def test_re_enable_restores_access(self, client, auth_headers, board_id, read_token):
        client.post(f"/api/v1/boards/{board_id}/sharing",
                    json={"enabled": True, "token": read_token},
                    headers=auth_headers)
        res = client.get(f"/api/v1/shared/boards/{read_token}")
        assert res.status_code == 200

    def test_delete_sharing_revokes_access(self, client, auth_headers, board_id, read_token):
        res = client.delete(f"/api/v1/boards/{board_id}/sharing", headers=auth_headers)
        assert res.status_code == 204
        res = client.get(f"/api/v1/shared/boards/{read_token}")
        assert res.status_code == 404


class TestSubscriptions:
    def test_create_subscription(self, client, auth_headers, board_id):
        res = client.post("/api/v1/subscriptions", json={
            "block_id": board_id,
            "subscriber_id": "some-user-id",
            "subscriber_type": "user",
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["blockId"] == board_id
        assert data["subscriberType"] == "user"

    def test_list_subscriptions_by_subscriber(self, client, auth_headers, board_id):
        res = client.get("/api/v1/subscriptions/some-user-id", headers=auth_headers)
        assert res.status_code == 200
        subs = res.json()
        assert any(s["blockId"] == board_id for s in subs)

    def test_delete_subscription(self, client, auth_headers, board_id):
        res = client.delete(f"/api/v1/subscriptions/{board_id}/some-user-id", headers=auth_headers)
        assert res.status_code == 204

        # No longer in list
        res = client.get("/api/v1/subscriptions/some-user-id", headers=auth_headers)
        assert all(s["blockId"] != board_id for s in res.json())
