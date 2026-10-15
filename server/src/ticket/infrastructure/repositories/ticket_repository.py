from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from src.ticket.application.ports.repositories import TicketRepositoryInterface
from src.ticket.domain.models.tickets import Ticket


class TicketRepository(TicketRepositoryInterface):
    """
    Implementation of TicketRepositoryInterface
    """

    def __init__(self, db: Session):
        self.db = db

    def list_tickets(self):
        tickets = self.db.execute(select(Ticket))
        return tickets.scalars()

    def create_ticket(self, title, description, category, priority, created_by):
        ticket = Ticket(title=title, description=description, category=category, priority=priority, created_by=created_by)
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
