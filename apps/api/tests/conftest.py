
import os
import tempfile
from pathlib import Path

# Configure an isolated SQLite database BEFORE importing
# any application module that initializes SQLAlchemy.

_test_directory = tempfile.TemporaryDirectory(
    prefix="aiops-tests-"
)

_test_db = Path(_test_directory.name) / "test.sqlite3"

os.environ["DATABASE_URL"] = (
    f"sqlite+pysqlite:///{_test_db}"
)

import pytest
from sqlalchemy import text

from app.database import engine
from app.models import Base


@pytest.fixture(scope="session", autouse=True)
def prepare_test_database():
    Base.metadata.create_all(bind=engine)

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO customers (id, name, email)
                VALUES (1, 'Test Customer', 'test@example.invalid')
                """
            )
        )

    yield
