# tests/conftest.py

import pytest
from app.database import Base, engine, SessionLocal, get_db  # <-- import get_db directly!
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="session", autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture()
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(db_session):
    def _get_db_override():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = _get_db_override  
    return TestClient(app)
