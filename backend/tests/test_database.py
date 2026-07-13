from sqlalchemy import text

from app.db.engine import engine


def test_database_connection_executes_select_one() -> None:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    assert result.scalar_one() == 1
