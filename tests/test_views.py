"""Integration tests — BC-Views (BoardView CRUD + filter/sort).

Covers:
- View creation with different viewTypes
- List views for a board
- Update view title and fields
- Delete view (soft-delete)
- Filtered card query (filter by property, sort by property, cardOrder)
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from nexo.db.base import Base
from nexo.db.session import get_db
from nexo.main import app

TEST_DB_URL = "sqlite:///./test_views.db"
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
        "username": "viewsuser", "email": "views@test.com", "password": "password123",
    })
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def board_id(client: TestClient, auth_headers: dict):
    res = client.post("/api/v1/teams", json={"title": "Views Team", "signupToken": ""}, headers=auth_headers)
    team_id = res.json()["id"]
    res = client.post("/api/v1/boards", json={"team_id": team_id, "title": "Views Board", "type": "P"}, headers=auth_headers)
    return res.json()["id"]


class TestViewCRUD:
    def test_create_kanban_view(self, client, auth_headers, board_id):
        res = client.post(f"/api/v1/boards/{board_id}/views", json={
            "board_id": board_id,
            "title": "My Kanban",
            "view_type": "board",
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["id"]
        assert data["title"] == "My Kanban"
        assert data["type"] == "view"
        assert data["createAt"] > 0

    def test_create_table_view(self, client, auth_headers, board_id):
        res = client.post(f"/api/v1/boards/{board_id}/views", json={
            "board_id": board_id,
            "title": "Table View",
            "view_type": "table",
        }, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["title"] == "Table View"

    def test_create_gallery_view(self, client, auth_headers, board_id):
        res = client.post(f"/api/v1/boards/{board_id}/views", json={
            "board_id": board_id,
            "title": "Gallery",
            "view_type": "gallery",
        }, headers=auth_headers)
        assert res.status_code == 200

    def test_create_calendar_view(self, client, auth_headers, board_id):
        res = client.post(f"/api/v1/boards/{board_id}/views", json={
            "board_id": board_id,
            "title": "Calendar",
            "view_type": "calendar",
        }, headers=auth_headers)
        assert res.status_code == 200

    def test_list_views_returns_all(self, client, auth_headers, board_id):
        res = client.get(f"/api/v1/boards/{board_id}/views", headers=auth_headers)
        assert res.status_code == 200
        views = res.json()
        titles = [v["title"] for v in views]
        assert "My Kanban" in titles
        assert "Table View" in titles
        assert "Gallery" in titles
        assert "Calendar" in titles

    def test_update_view_title(self, client, auth_headers, board_id):
        res = client.post(f"/api/v1/boards/{board_id}/views", json={
            "board_id": board_id, "title": "Old Title", "view_type": "board",
        }, headers=auth_headers)
        view_id = res.json()["id"]

        res = client.patch(f"/api/v1/boards/{board_id}/views/{view_id}",
                           json={"title": "New Title"}, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["title"] == "New Title"

    def test_update_view_fields(self, client, auth_headers, board_id):
        res = client.post(f"/api/v1/boards/{board_id}/views", json={
            "board_id": board_id, "title": "Filterable", "view_type": "table",
        }, headers=auth_headers)
        view_id = res.json()["id"]

        new_fields = {
            "view_type": "table",
            "filter": {"operation": "and", "filters": []},
            "sort_options": [],
            "card_order": [],
        }
        res = client.patch(f"/api/v1/boards/{board_id}/views/{view_id}",
                           json={"fields": new_fields}, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["fields"]["view_type"] == "table"

    def test_delete_view_removes_from_list(self, client, auth_headers, board_id):
        res = client.post(f"/api/v1/boards/{board_id}/views", json={
            "board_id": board_id, "title": "To Delete", "view_type": "board",
        }, headers=auth_headers)
        view_id = res.json()["id"]

        res = client.delete(f"/api/v1/boards/{board_id}/views/{view_id}", headers=auth_headers)
        assert res.status_code == 204

        res = client.get(f"/api/v1/boards/{board_id}/views", headers=auth_headers)
        ids = [v["id"] for v in res.json()]
        assert view_id not in ids

    def test_update_nonexistent_view_returns_404(self, client, auth_headers, board_id):
        res = client.patch(f"/api/v1/boards/{board_id}/views/nonexistent",
                           json={"title": "X"}, headers=auth_headers)
        assert res.status_code == 404


class TestFilteredCards:
    @pytest.fixture(scope="class")
    def setup(self, client, auth_headers, board_id):
        """Create a board with cards tagged with a 'status' property."""
        # Create a view
        res = client.post(f"/api/v1/boards/{board_id}/views", json={
            "board_id": board_id, "title": "Filter Test View", "view_type": "table",
        }, headers=auth_headers)
        view_id = res.json()["id"]

        # Create cards with properties
        card_a = client.post(f"/api/v1/boards/{board_id}/blocks", json={
            "board_id": board_id, "type": "card", "title": "Card A",
            "fields": {"properties": {"status": "done"}},
        }, headers=auth_headers).json()["id"]

        card_b = client.post(f"/api/v1/boards/{board_id}/blocks", json={
            "board_id": board_id, "type": "card", "title": "Card B",
            "fields": {"properties": {"status": "in-progress"}},
        }, headers=auth_headers).json()["id"]

        card_c = client.post(f"/api/v1/boards/{board_id}/blocks", json={
            "board_id": board_id, "type": "card", "title": "Card C",
            "fields": {"properties": {"status": "done"}},
        }, headers=auth_headers).json()["id"]

        return {"view_id": view_id, "card_a": card_a, "card_b": card_b, "card_c": card_c}

    def test_no_filter_returns_all_cards(self, client, auth_headers, board_id, setup):
        res = client.get(f"/api/v1/boards/{board_id}/views/{setup['view_id']}/cards",
                         headers=auth_headers)
        assert res.status_code == 200
        ids = [c["id"] for c in res.json()]
        assert setup["card_a"] in ids
        assert setup["card_b"] in ids
        assert setup["card_c"] in ids

    def test_filter_by_property_includes(self, client, auth_headers, board_id, setup):
        """Apply filter: status includes 'done' — should return A and C only."""
        filter_fields = {
            "view_type": "table",
            "filter": {
                "operation": "and",
                "filters": [
                    {
                        "filter_id": "f1",
                        "property_id": "status",
                        "condition": "includes",
                        "values": ["done"],
                    }
                ],
            },
            "sort_options": [],
            "card_order": [],
        }
        # Update view with filter
        client.patch(f"/api/v1/boards/{board_id}/views/{setup['view_id']}",
                     json={"fields": filter_fields}, headers=auth_headers)

        res = client.get(f"/api/v1/boards/{board_id}/views/{setup['view_id']}/cards",
                         headers=auth_headers)
        assert res.status_code == 200
        ids = [c["id"] for c in res.json()]
        assert setup["card_a"] in ids
        assert setup["card_c"] in ids
        assert setup["card_b"] not in ids

    def test_card_order_applied(self, client, auth_headers, board_id, setup):
        """Card order in fields should determine response order."""
        card_order = [setup["card_c"], setup["card_a"]]
        order_fields = {
            "view_type": "table",
            "filter": {"operation": "and", "filters": []},
            "sort_options": [],
            "card_order": card_order,
        }
        client.patch(f"/api/v1/boards/{board_id}/views/{setup['view_id']}",
                     json={"fields": order_fields}, headers=auth_headers)

        res = client.get(f"/api/v1/boards/{board_id}/views/{setup['view_id']}/cards",
                         headers=auth_headers)
        assert res.status_code == 200
        returned_ids = [c["id"] for c in res.json()]
        # C should come before A
        if setup["card_c"] in returned_ids and setup["card_a"] in returned_ids:
            assert returned_ids.index(setup["card_c"]) < returned_ids.index(setup["card_a"])
