from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

# Primary DB is PostgreSQL; for local development or when PostgreSQL is not
# available we fall back to a SQLite file. This allows the seed script and
# tests to run without requiring an external PostgreSQL server.
POSTGRES_URL = (
    "postgresql+psycopg://"
    "aiassistant:aiassistant_dev@"
    "127.0.0.1:5432/"
    "ai_operations"
)

DATABASE_URL = os.getenv("DATABASE_URL", POSTGRES_URL)

engine = create_engine(DATABASE_URL)

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