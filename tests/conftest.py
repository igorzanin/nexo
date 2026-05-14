import pytest
from fastapi.testclient import TestClient

from nexo.main import app
from nexo.db.session import engine, SessionLocal
from nexo.db.base import Base


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    client = TestClient(app)
    # Disable rate limiting for tests
    app.state.limiter.enabled = False
    return client


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
