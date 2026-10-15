from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID


class TicketBase(BaseModel):
    """Base schema for Ticket"""

    title: str
    description: str
    category: str
    priority: int


class TicketResponse(TicketBase):
    """Schema for ticket response"""

    id: UUID
    created_by: UUID

    model_config = ConfigDict(from_attributes=True)
