import uuid
from abc import ABC, abstractmethod
from typing import Optional
from src.ticket.domain.models.tickets import Ticket


class TicketRepositoryInterface(ABC):
    """
    Contract for TicketRepository
    """

    @abstractmethod
    def create_ticket(self, title: str, description: str, category: str, priority: int, created_by: uuid.UUID) -> Ticket:
        """Create a new ticket"""
        pass

    @abstractmethod
    def list_tickets(self) -> list[Ticket]:
        """List all tickets"""
        pass
