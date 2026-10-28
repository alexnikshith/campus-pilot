import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.models.base import Base
import app.models  # Ensure all models are registered on Base.metadata
from app.main import app as fastapi_app

# Use an in-memory SQLite database for isolated test execution
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionTest()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client():
    with TestClient(fastapi_app) as test_client:
        yield test_client
