from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Order


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.get("/")
def get_orders(
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Retrieve orders, optionally filtered by status or customer_id.

    Args:
        status: Filter orders by their status field.
        customer_id: Filter orders belonging to a specific customer.
        db: Database session dependency.
    """
    query = db.query(Order)
    if status is not None:
        query = query.filter(Order.status == status)
    if customer_id is not None:
        query = query.filter(Order.customer_id == customer_id)
    orders = query.all()
    return orders


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order