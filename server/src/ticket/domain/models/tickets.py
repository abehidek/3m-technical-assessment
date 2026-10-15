import uuid
from sqlalchemy import String, Integer, Uuid, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database import Base


class Ticket(Base):
    """
    Ticket entity
    """

    __tablename__ = "tickets"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[int] = mapped_column(String, nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id"), nullable=False
    )

    def __repr__(self):
        return f"<Ticket(id={self.id})>"