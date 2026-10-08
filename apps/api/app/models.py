from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
    )
    status = Column(String(30), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime)


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
    )
    subject = Column(String(255), nullable=False)
    status = Column(String(30), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime)
