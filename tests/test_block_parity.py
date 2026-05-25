"""Parity tests — BC-Content block CRUD (PT-003).

Cobre os cenários do arquivo parity_tests/03-block-crud.feature:
- Criar card com invariantes obrigatórios (id, createAt, updateAt > 0, board vinculado)
- Batch insert aceita blocos do mesmo board
- Batch insert com boards diferentes retorna erro
- Deletar card move snapshot para blocks_history
- Restaurar card reidrata o bloco deletado
- Deletar card inexistente não é erro
- Título do block respeita o máximo de 16383 runes
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from nexo.db.base import Base
from nexo.db.session import get_db
from nexo.main import app
from nexo.models.block import BlockHistory

TEST_DB_URL = "sqlite:///./test_block_parity.db"
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
        "username": "blockparity", "email": "blockparity@test.com", "password": "password123",
    })
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def board_and_team(client: TestClient, auth_headers: dict):
    res = client.post("/api/v1/teams", json={"title": "PT-003 Team", "signupToken": ""}, headers=auth_headers)
    assert res.status_code == 200
    team_id = res.json()["id"]

    res = client.post("/api/v1/boards", json={"team_id": team_id, "title": "PT-003 Board", "type": "P"}, headers=auth_headers)
    assert res.status_code == 200
    board_id = res.json()["id"]
    return team_id, board_id


class TestCreateCardInvariants:
    """Cenário: Criar card com invariantes obrigatórios."""

    def test_card_has_id_and_timestamps(self, client: TestClient, auth_headers: dict, board_and_team):
        _, board_id = board_and_team
        res = client.post(f"/api/v1/boards/{board_id}/blocks", json={
            "board_id": board_id,
            "type": "card",
            "title": "My Card",
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["id"]
        assert data["createAt"] > 0
        assert data["updateAt"] > 0

    def test_card_bound_to_board(self, client: TestClient, auth_headers: dict, board_and_team):
        _, board_id = board_and_team
        res = client.post(f"/api/v1/boards/{board_id}/blocks", json={
            "board_id": board_id,
            "type": "card",
            "title": "Board Check",
        }, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["boardId"] == board_id


class TestBatchInsert:
    """Cenários: Batch insert."""

    def test_batch_same_board(self, client: TestClient, auth_headers: dict, board_and_team):
        _, board_id = board_and_team
        res = client.post(f"/api/v1/boards/{board_id}/blocks/batch", json=[
            {"board_id": board_id, "type": "text", "title": "Block A"},
            {"board_id": board_id, "type": "text", "title": "Block B"},
        ], headers=auth_headers)
        assert res.status_code == 200
        blocks = res.json()
        assert len(blocks) == 2
        board_ids = {b["boardId"] for b in blocks}
        assert board_ids == {board_id}

    def test_batch_different_boards_rejected(self, client: TestClient, auth_headers: dict, board_and_team):
        team_id, board_id = board_and_team
        # Create second board
        res = client.post("/api/v1/boards", json={"team_id": team_id, "title": "Second Board", "type": "P"}, headers=auth_headers)
        board_id_2 = res.json()["id"]

        res = client.post(f"/api/v1/boards/{board_id}/blocks/batch", json=[
            {"board_id": board_id, "type": "text", "title": "Block A"},
            {"board_id": board_id_2, "type": "text", "title": "Block B"},
        ], headers=auth_headers)
        assert res.status_code == 400


class TestDeleteArchivesToHistory:
    """Cenário: Deletar card move o snapshot para histórico."""

    def test_delete_creates_history_entry(self, client: TestClient, auth_headers: dict, board_and_team):
        _, board_id = board_and_team
        res = client.post(f"/api/v1/boards/{board_id}/blocks", json={
            "board_id": board_id, "type": "card", "title": "To Delete",
        }, headers=auth_headers)
        block_id = res.json()["id"]

        res = client.delete(f"/api/v1/boards/{board_id}/blocks/{block_id}", headers=auth_headers)
        assert res.status_code == 204

        # Block no longer in active list
        res = client.get(f"/api/v1/boards/{board_id}/blocks", headers=auth_headers)
        active_ids = [b["id"] for b in res.json()]
        assert block_id not in active_ids

        # History entry exists in DB
        db = TestSession()
        try:
            stmt = select(BlockHistory).where(BlockHistory.id == block_id)
            entries = list(db.execute(stmt).scalars().all())
            assert len(entries) == 1
            assert entries[0].delete_at > 0
        finally:
            db.close()

    def test_deleted_block_has_delete_at_nonzero(self, client: TestClient, auth_headers: dict, board_and_team):
        _, board_id = board_and_team
        res = client.post(f"/api/v1/boards/{board_id}/blocks", json={
            "board_id": board_id, "type": "card", "title": "Delete Me Too",
        }, headers=auth_headers)
        block_id = res.json()["id"]

        client.delete(f"/api/v1/boards/{board_id}/blocks/{block_id}", headers=auth_headers)

        from nexo.models import Block
        db = TestSession()
        try:
            block = db.get(Block, block_id)
            assert block.delete_at > 0
        finally:
            db.close()


class TestRestoreBlock:
    """Cenário: Restaurar card reidrata o bloco deletado."""

    def test_undelete_restores_block(self, client: TestClient, auth_headers: dict, board_and_team):
        _, board_id = board_and_team
        res = client.post(f"/api/v1/boards/{board_id}/blocks", json={
            "board_id": board_id, "type": "card", "title": "Restore Me",
        }, headers=auth_headers)
        block_id = res.json()["id"]

        client.delete(f"/api/v1/boards/{board_id}/blocks/{block_id}", headers=auth_headers)

        res = client.post(f"/api/v1/boards/{board_id}/blocks/{block_id}/undelete", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["deleteAt"] == 0

        # Block appears in active list again
        res = client.get(f"/api/v1/boards/{board_id}/blocks", headers=auth_headers)
        active_ids = [b["id"] for b in res.json()]
        assert block_id in active_ids


class TestDeleteIdempotence:
    """Cenário: Deletar card inexistente não é erro."""

    def test_delete_nonexistent_is_ok(self, client: TestClient, auth_headers: dict, board_and_team):
        _, board_id = board_and_team
        res = client.delete(
            f"/api/v1/boards/{board_id}/blocks/nonexistent-id",
            headers=auth_headers,
        )
        assert res.status_code == 204


class TestTitleLength:
    """Cenário: Título do block respeita o máximo de 16383 runes."""

    def test_title_over_limit_rejected(self, client: TestClient, auth_headers: dict, board_and_team):
        _, board_id = board_and_team
        long_title = "a" * 16384
        res = client.post(f"/api/v1/boards/{board_id}/blocks", json={
            "board_id": board_id,
            "type": "text",
            "title": long_title,
        }, headers=auth_headers)
        assert res.status_code == 422

    def test_title_at_limit_accepted(self, client: TestClient, auth_headers: dict, board_and_team):
        _, board_id = board_and_team
        max_title = "a" * 16383
        res = client.post(f"/api/v1/boards/{board_id}/blocks", json={
            "board_id": board_id,
            "type": "text",
            "title": max_title,
        }, headers=auth_headers)
        assert res.status_code == 200
