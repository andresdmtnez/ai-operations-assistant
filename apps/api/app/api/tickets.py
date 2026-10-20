from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Ticket, Customer
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketResponse


router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)


@router.get("/", response_model=List[TicketResponse])
def get_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    return tickets


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return ticket


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    # Verify customer exists
    customer = db.query(Customer).filter(Customer.id == ticket.customer_id).first()
    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    # Create ticket with default status 'open'
    db_ticket = Ticket(
        customer_id=ticket.customer_id,
        subject=ticket.subject,
        description=ticket.description,
        status="open"
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket_status(
    ticket_id: int,
    ticket_update: TicketUpdate,
    db: Session = Depends(get_db)
):
    # Validate status
    valid_statuses = ["open", "in_progress", "closed"]
    if ticket_update.status not in valid_statuses:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid status. Must be one of {valid_statuses}"
        )

    # Get ticket
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Update status
    db_ticket.status = ticket_update.status
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

