from abc import ABC, abstractmethod
from typing import Optional
from src.auth.domain.models.user import User


class UserRepositoryInterface(ABC):
    """
    Contract for UserRepository
    """

    @abstractmethod
    async def create_user(self, email: str, hashed_password: str) -> User:
        """Create a new user"""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID"""
        pass
