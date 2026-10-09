"""Seed script for demo data
Location: apps/api/seed_data.py

This script creates deterministic demo data:
  - 500 customers
  - 2000 orders
  - 300 tickets

It can be executed safely multiple times – it will only insert missing records.
"""

import random
from sqlalchemy import func
from sqlalchemy.orm import Session

import sys
import os

# Ensure the FastAPI app package is importable when running this script from the project root.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.database import SessionLocal, engine
from app.models import Base, Customer, Order, Ticket


def get_counts(session: Session):
    return {
        "customers": session.query(func.count(Customer.id)).scalar(),
        "orders": session.query(func.count(Order.id)).scalar(),
        "tickets": session.query(func.count(Ticket.id)).scalar(),
    }


def create_customers(session: Session, target: int = 500):
    existing = session.query(func.count(Customer.id)).scalar()
    for i in range(existing + 1, target + 1):
        cust = Customer(
            name=f"Customer {i}",
            email=f"customer{i}@example.com",
        )
        session.add(cust)
    session.commit()


def create_orders(session: Session, target: int = 2000):
    existing = session.query(func.count(Order.id)).scalar()
    cust_count = session.query(func.count(Customer.id)).scalar()
    statuses = ["pending", "processing", "shipped", "cancelled"]
    for i in range(existing + 1, target + 1):
        order = Order(
            customer_id=((i - 1) % cust_count) + 1,
            status=random.choice(statuses),
            total_amount=round(random.uniform(10.0, 1000.0), 2),
        )
        session.add(order)
    session.commit()


def create_tickets(session: Session, target: int = 300):
    existing = session.query(func.count(Ticket.id)).scalar()
    cust_count = session.query(func.count(Customer.id)).scalar()
    statuses = ["open", "in_progress", "closed"]
    for i in range(existing + 1, target + 1):
        ticket = Ticket(
            customer_id=((i - 1) % cust_count) + 1,
            subject=f"Support ticket {i}",
            status=random.choice(statuses),
            description="Example support ticket generated for the development environment.",
        )
        session.add(ticket)
    session.commit()


def main():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        counts = get_counts(session)
        print("Current counts:", counts)
        if counts["customers"] < 500:
            print("Seeding customers...")
            create_customers(session, 500)
        if counts["orders"] < 2000:
            print("Seeding orders...")
            create_orders(session, 2000)
        if counts["tickets"] < 300:
            print("Seeding tickets...")
            create_tickets(session, 300)
        final_counts = get_counts(session)
        print("Final counts:", final_counts)
    finally:
        session.close()

if __name__ == "__main__":
    main()

