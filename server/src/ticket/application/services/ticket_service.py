from typing import Optional

from jose import JWTError, jwt
from pydantic import TypeAdapter
from src.auth.domain.models.user import User
from src.shared.config import settings
from src.auth.application.ports.repositories import UserRepositoryInterface
from src.ticket.application.ports.repositories import TicketRepositoryInterface
from src.ticket.domain.schemas.ticket_schemas import TicketBase, TicketResponse
from fastapi import HTTPException, status

ticket_list_adapter = TypeAdapter(list[TicketResponse])

class TicketService:
    """
    Business logic for Ticket
    """

    def __init__(self, user_repository: UserRepositoryInterface, ticket_repository: TicketRepositoryInterface):
        self.user_repo = user_repository
        self.ticket_repo = ticket_repository

    def verify_auth(self, token: str) -> Optional[User]:
        credentials_exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            email: str | None = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = self.user_repo.get_user_by_email(email)
        if user is None:
            raise credentials_exception

        return user

    def list_tickets(self, token: str) -> list[TicketResponse]:
        self.verify_auth(token)
        tickets = self.ticket_repo.list_tickets()
        return ticket_list_adapter.validate_python(tickets)

    def new_ticket(self, token: str, ticket_data: TicketBase) -> TicketResponse:
        user = self.verify_auth(token)
        ticket = self.ticket_repo.create_ticket(ticket_data.title, ticket_data.description, ticket_data.category, ticket_data.priority, user.id)
        return TicketResponse.model_validate(ticket)
     
        # if not user or not self._verify_password(password, user.hashed_password):
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Incorrect email or password",
        #         headers={"WWW-Authenticate": "Bearer"},
        #     )

