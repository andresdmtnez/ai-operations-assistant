from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

from app.api.customers import router as customers_router
from app.api.orders import router as orders_router
from app.api.tickets import router as tickets_router
from app.api.chat import router as chat_router

from .dependencies import get_db
from .models import Base
from .database import engine

app = FastAPI(
    title="AI Operations Assistant API",
    description="Operational API for the AI Operations Assistant",
    version="0.1.0",
)

# CORS configuration – allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure tables exist (create on startup)
Base.metadata.create_all(bind=engine)

@app.get("/health", tags=["health"])
def health(db: Session = Depends(get_db)):
    """Check API and database connectivity."""
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from exc

    return {"status": "ok"}

app.include_router(customers_router)
app.include_router(orders_router)
app.include_router(tickets_router)
app.include_router(chat_router)

