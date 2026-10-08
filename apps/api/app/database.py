from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    "postgresql+psycopg://"
    "aiassistant:aiassistant_dev@"
    "127.0.0.1:5432/"
    "ai_operations"
)

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