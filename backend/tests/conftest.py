from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.dependencies import get_db_session
from app.db.engine import engine
from app.main import create_application


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(
        bind=connection,
        autoflush=False,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    application = create_application()

    def override_db_session() -> Generator[Session, None, None]:
        yield db_session

    application.dependency_overrides[get_db_session] = override_db_session

    with TestClient(application) as test_client:
        yield test_client

    application.dependency_overrides.clear()
