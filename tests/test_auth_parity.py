"""Parity tests — BC-Identity auth flow (PT-001).

Cobre os cenários do arquivo parity_tests/01-auth.feature:
- Login com credenciais válidas retorna tokens
- Login com senha errada retorna 401
- Refresh emite novo access_token (novo token autoriza rota protegida)
- Logout invalida a sessão (token rejeitado depois)
- Token inválido/ausente retorna 401
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from nexo.db.base import Base
from nexo.db.session import get_db
from nexo.main import app

TEST_DB_URL = "sqlite:///./test_auth.db"
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
    """Reset slowapi storage before each test to avoid cross-test rate limit interference."""
    from limits.storage import MemoryStorage
    app.state.limiter._limiter.storage = MemoryStorage()
    yield


@pytest.fixture(scope="module")
def client():
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


@pytest.fixture(scope="module")
def user_creds(client: TestClient):
    """Register once; return (username, password, tokens)."""
    username = "parityuser"
    email = "parity@test.local"
    password = "parity1234"
    r = client.post("/api/v1/register", json={"username": username, "email": email, "password": password})
    assert r.status_code == 200, r.text
    return username, password, r.json()


# ── Cenário 1: Login com credenciais válidas ────────────────────────────────────

class TestLoginSuccess:
    def test_returns_access_token(self, client, user_creds):
        username, password, _ = user_creds
        r = client.post("/api/v1/login", json={"username": username, "password": password})
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_token_authorises_protected_route(self, client, user_creds):
        username, password, _ = user_creds
        r = client.post("/api/v1/login", json={"username": username, "password": password})
        token = r.json()["access_token"]
        r2 = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
        assert r2.status_code == 200
        assert r2.json()["username"] == username


# ── Cenário 2: Login com senha errada ──────────────────────────────────────────

class TestLoginFailure:
    def test_wrong_password_returns_401(self, client, user_creds):
        username, _, _ = user_creds
        r = client.post("/api/v1/login", json={"username": username, "password": "wrongpass"})
        assert r.status_code == 401

    def test_unknown_user_returns_401(self, client):
        r = client.post("/api/v1/login", json={"username": "nobody", "password": "whatever"})
        assert r.status_code == 401


# ── Cenário 3: Refresh renova sessão ───────────────────────────────────────────

class TestRefresh:
    def test_refresh_issues_new_access_token(self, client, user_creds):
        username, password, _ = user_creds
        login = client.post("/api/v1/login", json={"username": username, "password": password})
        tokens = login.json()
        r = client.post("/api/v1/refresh", json={"refresh_token": tokens["refresh_token"]})
        assert r.status_code == 200
        new = r.json()
        assert "access_token" in new
        assert new["access_token"] != tokens["access_token"]

    def test_new_token_authorises_protected_route(self, client, user_creds):
        username, password, _ = user_creds
        login = client.post("/api/v1/login", json={"username": username, "password": password})
        r = client.post("/api/v1/refresh", json={"refresh_token": login.json()["refresh_token"]})
        new_token = r.json()["access_token"]
        r2 = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {new_token}"})
        assert r2.status_code == 200

    def test_invalid_refresh_token_returns_401(self, client):
        r = client.post("/api/v1/refresh", json={"refresh_token": "bad.token.here"})
        assert r.status_code == 401


# ── Cenário 4: Logout invalida sessão ──────────────────────────────────────────

class TestLogout:
    def test_logout_then_token_rejected(self, client, user_creds):
        username, password, _ = user_creds
        login = client.post("/api/v1/login", json={"username": username, "password": password})
        token = login.json()["access_token"]

        # Confirma que o token funciona
        r_before = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
        assert r_before.status_code == 200

        # Logout
        r_logout = client.post("/api/v1/logout", headers={"Authorization": f"Bearer {token}"})
        assert r_logout.status_code == 204

        # Token deve ser rejeitado
        r_after = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
        assert r_after.status_code == 401


# ── Cenário 5: Token inválido / ausente ────────────────────────────────────────

class TestInvalidToken:
    def test_no_token_returns_401(self, client):
        r = client.get("/api/v1/users/me")
        assert r.status_code == 401

    def test_malformed_token_returns_401(self, client):
        r = client.get("/api/v1/users/me", headers={"Authorization": "Bearer not.a.jwt"})
        assert r.status_code == 401

    def test_access_token_used_as_refresh_returns_401(self, client, user_creds):
        username, password, _ = user_creds
        login = client.post("/api/v1/login", json={"username": username, "password": password})
        access = login.json()["access_token"]
        r = client.post("/api/v1/refresh", json={"refresh_token": access})
        assert r.status_code == 401
