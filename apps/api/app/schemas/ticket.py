from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class TicketBase(BaseModel):
    subject: str = Field(..., max_length=255, description="Subject of the ticket")
    description: Optional[str] = Field(None, description="Detailed description of the ticket")


class TicketCreate(TicketBase):
    customer_id: int = Field(..., gt=0, description="ID of the customer associated with the ticket")


class TicketUpdate(BaseModel):
    status: str = Field(..., description="Status of the ticket (open, in_progress, closed)")


class TicketResponse(TicketBase):
    id: int
    customer_id: int
    status: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
