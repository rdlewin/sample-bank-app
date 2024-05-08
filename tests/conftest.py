import pytest
from fastapi.testclient import TestClient
from pydantic_core import Url
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from src.core.config import settings
from src.core.db import Base, get_db
from src.main import app

TEST_DATABASE_URI = Url.build(
    scheme="postgresql",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_SERVER,
    port=settings.POSTGRES_PORT,
    path="test_db",
)
engine = create_engine(TEST_DATABASE_URI.unicode_string(), echo=False)
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.drop_all(engine)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
Base.metadata.create_all(engine)


def override_get_db() -> Session:
    db = TestingSessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client() -> TestClient:
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


from fixtures import (  # noqa: F401
    account,
    account_service,
    transaction_service,
    user,
    user_service,
)
