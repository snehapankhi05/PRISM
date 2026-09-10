import pytest

from backend.app.db.session import SessionLocal


@pytest.fixture
def db_session():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.rollback()
        db.close()