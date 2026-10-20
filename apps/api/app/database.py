
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL must be provided through environment variables.
# Production/development: PostgreSQL
# Isolated tests: SQLite, when explicitly configured.

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL no está definida. "
        "Configura la conexión a la base de datos."
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
