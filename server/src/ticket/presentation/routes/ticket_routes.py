from fastapi import APIRouter, Depends, Response, Cookie, status
from sqlalchemy.orm import Session
from typing import Optional

from src.shared.database import get_db
from src.ticket.domain.schemas.ticket_schemas import (
    TicketBase,
    TicketResponse
)
from src.auth.infrastructure.repositories.user_repository import UserRepository
from src.ticket.infrastructure.repositories.ticket_repository import TicketRepository
from src.ticket.application.services.ticket_service import TicketService

router = APIRouter(prefix="/ticket", tags=["Ticket"])


def get_ticket_service(db: Session = Depends(get_db)) -> TicketService:
    """
    Creates AuthService with deps
    """
    user_repository = UserRepository(db)
    ticket_repository = TicketRepository(db)
    return TicketService(user_repository, ticket_repository)


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def register(
    *,
    access_token: Optional[str] = Cookie(None),
    ticket_data: TicketBase,
    ticket_service: TicketService = Depends(get_ticket_service)
):
    """
    Creates a new Ticket
    """

    if not access_token:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    return ticket_service.new_ticket(access_token, ticket_data)

@router.get("/", response_model=list[TicketResponse], status_code=status.HTTP_200_OK)
def register(
    access_token: Optional[str] = Cookie(None),
    ticket_service: TicketService = Depends(get_ticket_service)
):
    """
    Creates a new Ticket
    """

    if not access_token:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    return ticket_service.list_tickets(access_token)