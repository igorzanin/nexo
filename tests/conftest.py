import pytest
from fastapi.testclient import TestClient
from limits.storage import MemoryStorage

from nexo.main import app
from nexo.db.session import engine, SessionLocal
from nexo.db.base import Base


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    app.state.limiter._limiter.storage = MemoryStorage()
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
